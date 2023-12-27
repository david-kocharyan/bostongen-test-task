import tempfile

from fastapi import APIRouter, File, UploadFile, Query
from starlette.responses import JSONResponse

from app.models import MD5Result, MD5Status
from app.tasks import calculate_md5
from app.database import get_db

from app.utils import generate_unique_promise_id

router = APIRouter()


@router.post("/upload-file/", name="Upload File")
async def upload_file(file: UploadFile = File()):
    promise_id = generate_unique_promise_id()

    with tempfile.NamedTemporaryFile(delete=False, dir='/tmp') as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    calculate_md5.apply_async(args=[temp_file_path, promise_id])

    return JSONResponse(content={"promise_id": promise_id}, status_code=200)


@router.get("/get-result/{promise_id}", name="Get result by promise_id")
async def get_result(promise_id: str):
    db = get_db()
    result = db.query(MD5Result).filter(MD5Result.promise_id == promise_id).first()

    if result:
        if result.status == MD5Status.SUCCESS:
            return JSONResponse(
                content={
                    "id": result.id,
                    "md5_hash": result.md5_hash,
                    "status": MD5Status.SUCCESS.value
                },
                status_code=200
            )
        elif result.status == MD5Status.PENDING:
            return JSONResponse(
                content={
                    "status": MD5Status.PENDING.value
                },
                status_code=200
            )
        else:
            return JSONResponse(
                content={
                    "status": MD5Status.FAILED.value
                },
                status_code=500
            )
    else:
        return JSONResponse(content={}, status_code=400)


@router.get("/get-all-results", name="Get all results")
async def get_all_results(offset: int = Query(0, ge=0), limit: int = Query(10, le=100)):
    db = get_db()

    results_query = db.query(MD5Result)
    total_items = results_query.count()

    results = results_query.offset(offset).limit(limit).all()

    if results:
        response_data = []
        for result in results:
            response_data.append({
                "id": result.id,
                "promise_id": result.promise_id,
                "md5_hash": result.md5_hash,
                "status": result.status.value
            })

        return JSONResponse(
            content={
                "items": response_data,
                "total_items": total_items,
                "page": offset // limit + 1,  # Current page
                "total_pages": (total_items + limit - 1) // limit  # Total pages
            },
            status_code=200
        )
    else:
        return JSONResponse(content={"items": [], "total_items": 0, "page": 1, "total_pages": 0}, status_code=404)

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Optional, List
from datetime import datetime

from . import models, schemas, security
from app.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not security.verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def create_report(db: Session, report: schemas.ReportCreate, user_id: int):
    db_report = models.Report(**report.dict(), owner_id=user_id)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def get_user_reports(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Report).filter(
        models.Report.owner_id == user_id
    ).offset(skip).limit(limit).all()

def create_scan_job(db: Session, scan_job: schemas.ScanJobCreate, user_id: int):
    db_scan_job = models.ScanJob(
        **scan_job.dict(),
        owner_id=user_id,
        status="pending"
    )
    db.add(db_scan_job)
    db.commit()
    db.refresh(db_scan_job)
    return db_scan_job

def get_scan_job(db: Session, job_id: int):
    return db.query(models.ScanJob).filter(models.ScanJob.id == job_id).first()

def update_scan_job_status(db: Session, job_id: int, status: str, report_id: Optional[int] = None):
    db_job = get_scan_job(db, job_id)
    if db_job:
        db_job.status = status
        if report_id:
            db_job.report_id = report_id
        if status in ["completed", "failed"]:
            db_job.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(db_job)
    return db_job 
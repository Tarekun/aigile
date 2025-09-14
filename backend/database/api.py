from database.config import get_db
from database.schemas import Issue, convert_issue
from version_control.interface import Issue as VCIssue


def store_issue(issue: VCIssue):
    issue = convert_issue(issue)
    db = next(get_db())
    try:
        db.add(issue)
        db.commit()
        db.refresh(issue)
    finally:
        db.close()

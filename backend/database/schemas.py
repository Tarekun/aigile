from sqlalchemy import Column, Integer, String, Text, ARRAY
from database.config import Base
from version_control.interface import Issue as VCIssue


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    state = Column(String, nullable=False)
    url = Column(String)
    labels = Column(ARRAY(String))


def convert_issue(issue: VCIssue):
    return Issue(
        id=issue.id,
        title=issue.title,
        description=issue.description,
        state=issue.state,
        url=issue.url,
        labels=issue.labels,
    )

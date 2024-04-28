from sqlalchemy import select, desc
from sqlalchemy.sql.expression import collate

from src.repository.models import (
    Sex,
    Individ,
    Researcher,
    ArchaeologicalSite,
    Epoch,
    Preservation,
    Region,
    User
    )


def sort_func(column_name, filter=None):
    stmt = select(Individ)
    if not column_name:
        column_name = 'index'
    if filter:
        stmt = stmt.filter_by(**filter)
    match column_name:
        case 'id':
            stmt = stmt.order_by(
                Individ.id
            )
        case 'index':
            stmt = stmt.order_by(
                collate(Individ.index, "numeric")
            )
        case 'researcher':
            stmt = stmt.join(
                ArchaeologicalSite
                ).join(
                    ArchaeologicalSite.researchers
                    ).group_by(
                        Individ.id, Researcher.last_name
                        ).order_by(
                            Researcher.last_name,
                            collate(Individ.index, "numeric")
                            )
        case 'site':
            stmt = stmt.join(ArchaeologicalSite).order_by(
                    ArchaeologicalSite.name,
                    collate(Individ.index, "numeric")
                )
        case 'region':
            stmt = stmt.join(
                ArchaeologicalSite
            ).join(
                ArchaeologicalSite.region).group_by(
                    Individ.id, Region.name
                ).order_by(
                    Region.name,
                    collate(Individ.index, "numeric")
                )
        case 'sex':
            stmt = stmt.join(
                Individ.sex
            ).order_by(
                Sex.sex,
                collate(Individ.index, "numeric")
            )
        case 'type':
            stmt = stmt.order_by(
                Individ.type,
                collate(Individ.index, "numeric")
            )
        case "preservation":
            stmt = stmt.join(
                Individ.preservation
                ).order_by(
                    Preservation.id,
                    collate(Individ.index, "numeric")
                )
        case "epoch":
            stmt = stmt.join(
                Individ.epoch).order_by(
                    Epoch.name,
                    collate(Individ.index, "numeric")
            )
        case "creator":
            stmt = stmt.join(
                Individ.creator).order_by(
                    User.last_name,
                    collate(Individ.index, "numeric")
            )
        case "editor":
            stmt = stmt.join(
                Individ.editor).order_by(
                    User.last_name,
                    collate(Individ.index, "numeric")
            )
        case "created_at":
            stmt = stmt.order_by(
                desc(Individ.created_at)
            )
    return stmt

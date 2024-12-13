from src.repository.models import Individ, ArchaeologicalSite, Epoch, Preservation, Country, Grave, User, Researcher, Sex, Region

from sqlalchemy import select, or_, between, case


def filtering(filters):

    stmt = select(Individ).join(Individ.site).join(Individ.preservation).join(ArchaeologicalSite.researchers).join(Individ.sex).join(ArchaeologicalSite.region)
    if index_search_filter := filters.get('index'):
        stmt = stmt.where(Individ.index.ilike(f'%{index_search_filter}%'))
    if epoch_filter := filters.get('epoch'):
        stmt = stmt.join(Individ.epoch).where(getattr(Epoch, 'id').in_(epoch_filter))
    if researcher_filter := filters.get('researcher'):
        stmt = stmt.where(getattr(Researcher, 'id').in_(researcher_filter))
    if country_filter := filters.get('country'):
        stmt = stmt.join(Region.country).where(getattr(Country, 'id').in_(country_filter))
    if year_min_filter := filters.get('year_min'):
        stmt = stmt.where(Individ.year >= year_min_filter)
    if year_max_filter := filters.get('year_max'):
        stmt = stmt.where(Individ.year <= year_max_filter)
    if sex_filter := filters.get('sex'):
        stmt = stmt.where(getattr(Sex, 'sex').in_(sex_filter))
    if preservation_filter := filters.get('preservation'):
        stmt = stmt.where(getattr(Preservation, 'id').in_(preservation_filter))
    if grave_type_filter := filters.get('grave_type'):
        stmt = stmt.join(Individ.grave).where(getattr(Grave, 'grave_type').in_(grave_type_filter))
    if creator_filter := filters.get('creator'):
        stmt = stmt.join(Individ.creator).where(getattr(User, 'id').in_(creator_filter))
    if arch_site_filter := filters.get('site'):
        stmt = stmt.join(Individ.site).where(getattr(ArchaeologicalSite, 'id').in_(arch_site_filter))
    if type_filter := filters.get('type'):
        stmt = stmt.where(getattr(Individ, 'type').in_(type_filter))
    if grave_number_filter := filters.get('grave'):
        stmt = stmt.join(Individ.grave).where(getattr(Grave, 'grave_number').in_(grave_number_filter))
    if comment_filter := filters.get('comment'):
        stmt = stmt.join(Individ.comment).where(Individ.comment.ilike(f'%{comment_filter}%'))
    if filters.get('age_min') and filters.get('age_max'):
        age_min = filters.get('age_min')
        age_max = filters.get('age_max')
        stmt = stmt.where(
            case(
                (Individ.age_max.is_(None), or_(between(Individ.age_min, age_min, age_max), Individ.age_min < age_min)),
                (Individ.age_min.is_(None), Individ.age_max >= age_min),
                else_=(or_(between(Individ.age_min, age_min, age_max), between(Individ.age_max, age_min, age_max)))
            )
            )
    if filters.get('age_min') and not filters.get('age_max'):
        age_min = filters.get('age_min')
        stmt = stmt.where(
            case(
                (Individ.age_max.is_(None), Individ.age_min >= 0),
                else_=or_(between(Individ.age_min, age_min, 200), between(Individ.age_max, age_min, 200))
                )
            )
    if filters.get('age_max') and not filters.get('age_min'):
        age_max = filters.get('age_max')
        stmt = stmt.where(
            case(
                (Individ.age_min.is_(None), Individ.age_max > 0),
                else_=or_(between(Individ.age_max, 0, age_max), Individ.age_min <= age_max)
                )
            )
    # global individs
    stmt = stmt.group_by(Individ.id).order_by(Individ.index)
    return stmt
    # individs = session.scalars(stmt).all()
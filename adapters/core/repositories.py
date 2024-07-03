from abc import ABC

from core.pagination import MAX_LIMIT


class ChildMeta(ABC):
    columns: tuple[str]


class PgRepository:

    def _get_child_meta(self) -> ChildMeta:
        try:
            meta: ChildMeta = getattr(self, 'Meta')
        except AttributeError:
            raise NotImplementedError
        return meta

    def columns(self):
        meta = self._get_child_meta()
        return ', '.join(meta.columns)

    def order_by(
        self,
        order_by: str | None,
        stmt: str,
        args: list,
    ):
        meta = self._get_child_meta()
        
        if order_by:
            order_field = order_by[1:] if order_by.startswith('-') else order_by
            order_field = order_field if order_field in meta.columns else 'id'
            stmt += f'ORDER BY {order_field} '

            order_type = 'DESC ' if order_by.startswith('-') else 'ASC '
            stmt += order_type
        return stmt, args

    def limit(
        self,
        limit: int | None,
        stmt: str,
        args: list,
    ):
        if not limit or limit <= 0:
            limit = MAX_LIMIT
        args.append(limit)
        stmt += f'LIMIT ${len(args)}'

        return stmt, args
    
    def offset(
        self,
        offset: int | None,
        stmt: str,
        args: list,
    ):
        if not offset or offset < 0:
            offset = 0
        args.append(offset)
        stmt += f'OFFSET ${len(args)}'

        return stmt, args
    

from weather.services import ServiceBaseDetail
from webargs import fields, validate
from webargs.tornadoparser import parser
from weather import config


class MixinDetail(ServiceBaseDetail):
    carrier = None

    async def agreement(self, request):
        agreement = {
            "target": fields.Str(validate=validate.Length(min=1), required=True),
            "value": fields.Str(validate=validate.Length(min=1), required=True),
            "page": fields.Int(default=0),
            "page_size": fields.Int(default=config.PAGE_SIZE)}

        params = parser.parse(agreement, request, location="query")
        return params

    async def _run_process(self, params):
        target, value = str(params.get('target')).lower(), str(params.get('value')).lower()
        page, size = params.get('page'), params.get('page_size')

        result = await self.query_mount(target, value, page, size)

        data = {
            'resultsCount': result.total,
            'next_page': result.next_page,
            'previous_page': result.previous_page,
            'data': [await self.result_mount(obj) for obj in result.items]
        }

        return data

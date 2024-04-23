# from scrapy.dupefilters import RFPDupeFilter
# from asgiref.sync import sync_to_async
# from proj.hotdeal.models import ScrappingModel  # Django 모델 임포트

# class CustomDupeFilter(RFPDupeFilter):
#     @sync_to_async
#     def request_seen(self, request):
#         if ScrappingModel.objects.filter(url=request.url).exists():
#             # URL이 이미 데이터베이스에 존재하면 중복으로 처리하고 중단 신호를 보냄
#             return True
#         else:
#             return super().request_seen(request)
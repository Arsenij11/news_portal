# from .models import Post,PostCategory,Category
#
# post = Post.objects.get(pk=1)
# post_categories = PostCategory.objects.filter(post_id_id=1)
# categories = []
# for post_category in post_categories:
#     categories.append(Category.objects.get(pk=post_category.category_id_id))
# subscribers = {}
#
# for category in categories:
#     subscribers[category.category_name] = []
#     all_subs = category.subscribers.all()
#     subscribers[category.category_name].append(s.email for s in all_subs)
#
# for name_category, emails in subscribers.items():
#     for email in emails:
#         print(email)
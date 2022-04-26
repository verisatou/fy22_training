from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from .models import Feedback
from .models import Reply
from .forms import FeedbackForm
from .forms import ReplyForm
from django.template import loader
from django.shortcuts import get_object_or_404
#loginの制限
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from login.models import CustomUser

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.views.decorators.http import require_POST

#mypage-------------------feedback/index
@login_required
def index(request):
    template = loader.get_template('feedback/mypage.html')
    context = { }
    return render(request, 'feedback/mypage.html', context)

# Feedbackの【個人宛一覧】表示機能-------------------feedback/private_list
class FeedbackPrivateListView(LoginRequiredMixin,generic.ListView):
    model = Feedback
    template_name="feedback/private_list.html"
 
    #ログインしたユーザー宛のフィードバックだけFeedbackmodelから抽出、カテゴリを変更した際にはこの関数は呼び出されない
    def get_context_data(self, *args, **kwargs):
        filter_category = "default"

        object_list = Feedback.objects.filter(user_id__id__exact = self.request.user.id)

        context = {
            'object_list' : object_list,
            'category' : filter_category,   #初期カテゴリ名
            'object_category' : Feedback.objects.filter(user_id__id__exact = self.request.user.id) #カテゴリ名表示用
        }
        return context
  
    # カテゴリ別にフィードバックを抽出する関数
    def post(self, request, *args, **kwargs):

        filter_category = request.POST.get('filer_ctg') #送られてきたカテゴリ名をゲット

        #送られてきたカテゴリ名がすべて、もしくはカテゴリ表示だったらすべてのフィードバックを表示
        if filter_category == "all":
            object_list =Feedback.objects.filter(user_id__id__exact = self.request.user.id)
        else:
            object_list =Feedback.objects.filter(user_id__id__exact = self.request.user.id).filter(category=filter_category)

        context = {
            'category' : filter_category,
            'object_list' : object_list,
            'object_category' : Feedback.objects.filter(user_id__id__exact = self.request.user.id),#カテゴリ名表示用
        }
        return render(request, 'feedback/private_list.html', context)


# Feedbackの【個人宛詳細】表示機能-------------------feedback/private_detail
class FeedbackPrivateReplyDetailView(LoginRequiredMixin,generic.FormView):
    model = Feedback
    template_name = "feedback/feedback_private_detail.html"
    form_class = ReplyForm

    #Feedbackモデルに加えて、replyモデルを使うために上書き
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'feedback': Feedback.objects.filter(user_id__id__exact = self.request.user.id).filter(id=self.kwargs['pk']),
            'reply': Reply.objects.filter(feedback_id__id=self.kwargs['pk']),
            'feedback_count': Feedback.objects.filter(user_id__id__exact = self.request.user.id).filter(id=self.kwargs['pk']).count(),
        })
        return context

    # feedback_idの欄を自動でfeedback_にする
    def form_valid(self, form):
        feedback_pk = get_object_or_404(Feedback, pk=self.kwargs.get('pk'))
        form.instance.feedback_id=feedback_pk
        form.instance.replyer = self.request.user
        #保存せずオブジェクト生成する
        comment = form.save(commit=False)
        #保存
        comment.save()
        return super(FeedbackPrivateReplyDetailView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('feedback:private_detail', kwargs={'pk': self.kwargs['pk']})
    

# Feedbackの【全体宛一覧】表示機能-------------------feedback/list
class FeedbackListView(LoginRequiredMixin,generic.ListView):
    model = Feedback
   

    #全体宛のフィードバックだけFeedbackmodelから抽出、カテゴリを変更した際にはこの関数は呼び出されない
    #ここでの1とはアカウント作成順である
    def get_context_data(self, *args, **kwargs):
        filter_category = "default"

        object_list =Feedback.objects.filter(user_id__id=1)

        context = {
            'object_list' : object_list,
            'category' : filter_category,   #初期カテゴリ名
            'object_category' : Feedback.objects.filter(user_id__id=1),#カテゴリ名表示用
        }
        return context
  
    # カテゴリ別にフィードバックを抽出する関数
    def post(self, request, *args, **kwargs):

        filter_category = request.POST.get('filer_ctg') #送られてきたカテゴリ名をゲット

        #送られてきたカテゴリ名がすべて、もしくはカテゴリ表示だったらすべてのフィードバックを表示
        if filter_category == "all" or filter_category == "default":
            object_list =Feedback.objects.filter(user_id__id=1)
        else:
            object_list =Feedback.objects.filter(user_id__id=1).filter(category=filter_category)

        context = {
            'category' : filter_category,
            'object_list' : object_list,
            'object_category' : Feedback.objects.filter(user_id__id=1),#カテゴリ名表示用
        }
        return render(request, 'feedback/feedback_list.html', context)


# Feedbackの【全体詳細】表示機能-------------------feedback/detail
class FeedbackDetailView(LoginRequiredMixin,generic.FormView):
    model = Feedback
    template_name="feedback/feedback_detail.html"
    form_class = ReplyForm
    
    #Feedbackモデルに加えて、replyモデルを使うために上書き
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'feedback': Feedback.objects.filter(user_id__id=1).filter(id=self.kwargs['pk']),
            'reply': Reply.objects.filter(feedback_id__id=self.kwargs['pk']),
            'feedback_count': Feedback.objects.filter(user_id__id=1).filter(id=self.kwargs['pk']).count(),
        })
        return context

    # feedback_idの欄を自動でfeedback_にする
    def form_valid(self, form):
        feedback_pk = get_object_or_404(Feedback, pk=self.kwargs.get('pk'))
        form.instance.feedback_id=feedback_pk
        form.instance.replyer = self.request.user
        #保存せずオブジェクト生成する
        comment = form.save(commit=False)
        #保存
        comment.save()
        return super(FeedbackDetailView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('feedback:detail', kwargs={'pk': self.kwargs['pk']})

# Feedbackの【投稿】機能-------------------feedback/create
class FeedbackCreateView(LoginRequiredMixin,generic.CreateView):
    model = Feedback
    form_class = FeedbackForm

    #呼び出される際にHTMLに送るデータ
    def get_context_data(self, *args, **kwargs):
        context = {
            'form' : FeedbackForm,
            'user' : CustomUser.objects.all(),
            'model' : Feedback,
        }
        return context


    #フィードバックを新規作成(文字カウントのため自作)
    def post(self,request):
        
        #チェックボックスの出力値はon、offからbool値に変換
        if request.POST['anonymous'] == "on":
            anonymous = True
        else:
            anonymous = False

        #POSTメソッドで呼び出されたら
        if request.method == 'POST':
            #新規フィードバック作成
            Feedback.objects.create(
                title = request.POST['title'],
                user_id = CustomUser(id=request.POST['user_id']),
                sender = str(self.request.user),
                content = request.POST['content'],
                anonymous = anonymous,
                category = request.POST['category'],
            )
    
            #投稿完了画面に遷移するための処理        
            create_user = Feedback.objects.filter(sender = self.request.user.username)
            create_id= create_user.latest("created_at").id
            # create_id= create_user.order_by("id").last().id
            return redirect('feedback:history_detail', pk=create_id)

# Feedbackの【投稿】機能-------------------feedback/create
# class FeedbackCreateView(LoginRequiredMixin,generic.CreateView):
#     model = Feedback
#     form_class = FeedbackForm
#     #senderの欄を自動でログインユーザーにする
#     def form_valid(self, form):
#         form.instance.sender = self.request.user
#         return super(FeedbackCreateView, self).form_valid(form)

#     def get_success_url(self):
#         #送り主＝ログインユーザー　の最後のレコードを表示する
#         create_user = Feedback.objects.filter(sender = self.request.user.username)
#         # create_id= create_user.latest("created_at").id
#         create_id= create_user.order_by("id").last().id
#         return reverse_lazy('feedback:history_detail', kwargs={'pk':create_id})

# Feedbackの【編集】機能-------------------feedback/update
class FeedbackUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = Feedback
    form_class = FeedbackForm
    #呼び出される際にHTMLに送るデータ
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form' : FeedbackForm,
            'user' : CustomUser.objects.all(),
            'model' : Feedback,
        })
        return context

    def get_queryset(self, *args, **kwargs):
        object =Feedback.objects.filter(sender = self.request.user.username)
        return object

    
    #フィードバック編集(文字カウントのため自作)
    def post(self,request,pk):

        
        #チェックボックスの出力値はon、offからbool値に変換
        if request.POST['anonymous'] == 'on':
            anonymous = True
        else:
            anonymous = False

        #POSTメソッドで呼び出されたら
        if request.method == 'POST':
            feedback = Feedback.objects.get(pk =self.kwargs['pk'])
            #フィードバック編集
            feedback.title = request.POST['title']
            feedback.user_id = CustomUser(id=request.POST['user_id'])
            feedback.sender = str(self.request.user)
            feedback.content = request.POST['content']
            feedback.anonymous = anonymous
            feedback.category = request.POST['category']
            feedback.save()
    
        #投稿履歴の詳細画面に遷移するための処理        
        return redirect('feedback:history_detail', pk=self.kwargs['pk'])

# Feedbackの削除機能-------------------#
class FeedbackDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = Feedback
    success_url = reverse_lazy('feedback:complete')

#Feedbackの【投稿履歴一覧】表示機能-------------------feedback/history
class FeedbackHistoryListView(LoginRequiredMixin,generic.ListView):
    model = Feedback
    template_name="feedback/feedback_history_list.html"
    #sender 送り主とログインユーザー名が一緒だったらリストに表示する
    def get_queryset(self, *args, **kwargs):
        object_list =Feedback.objects.filter(sender = self.request.user)
        return object_list

#Feedbackの【投稿履歴詳細】機能-------------------feedback/history_detail
class FeedbackHistoryDetailView(LoginRequiredMixin,generic.FormView):
    model = Feedback
    template_name="feedback/feedback_history_detail.html"
    form_class = ReplyForm

    #Feedbackモデルに加えて、replyモデルを使うために上書き
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'feedback': Feedback.objects.filter(sender = self.request.user).filter(id=self.kwargs['pk']),
            'reply': Reply.objects.filter(feedback_id__id=self.kwargs['pk']),
            'feedback_count': Feedback.objects.filter(sender = self.request.user).filter(id=self.kwargs['pk']).count(),
        })
        return context

    # feedback_idの欄を自動でfeedback_にする
    def form_valid(self, form):
        feedback_pk = get_object_or_404(Feedback, pk=self.kwargs.get('pk'))
        form.instance.feedback_id=feedback_pk
        form.instance.replyer = self.request.user
        #保存せずオブジェクト生成する
        comment = form.save(commit=False)
        #保存
        comment.save()
        return super(FeedbackHistoryDetailView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('feedback:history_detail', kwargs={'pk': self.kwargs['pk']})

#返信の作成機能-------------------feedback/reply_create
class ReplyCreateView(LoginRequiredMixin,generic.CreateView):
    model = Reply
    form_class = ReplyForm

    # feedback_idの欄を自動でfeedback_にする
    def form_valid(self, form):
        feedback_pk = get_object_or_404(Feedback, pk=self.kwargs.get('pk'))
        form.instance.feedback_id=feedback_pk
        form.instance.replyer = self.request.user
        return super(ReplyCreateView, self).form_valid(form)

    success_url = reverse_lazy('feedback:complete')

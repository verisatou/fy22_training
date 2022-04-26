from django.views import generic
from django.urls import reverse_lazy
from .models import Memo
from .forms import MemoForm
#loginの制限
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from login.models import CustomUser
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.views.decorators.http import require_POST

# Memoの一覧表示機能
class MemoListView(LoginRequiredMixin,generic.ListView):
    model = Memo

    #ログインしたユーザーのメモだけを抽出する
    def get_queryset(self, *args, **kwargs):
        object_list =Memo.objects.filter(user_id__id__exact = self.request.user.id)
        return object_list

    #達成未達成ステータスの更新
    def post(self, request):
        status_value = ""
        pk = 0
        i = 0

        #送られてきたメモのpkを取得する
        while True:
            pk = str(i)
            status_value = request.POST.get(pk)
            if status_value != None:
                break
            i += 1

        #取得したpkのメモ情報を取り出しステータスを達成、未達成に変更する
        memo = Memo.objects.get(pk = pk)
        memo.status = status_value
        memo.save()

        # 一覧ページにリダイレクト
        return redirect('memo:list')  

# Memoの詳細表示機能
class MemoDetailView(LoginRequiredMixin,generic.DetailView):
    model = Memo

    #自分のメモしか編集できないようにフィルター
    def get_queryset(self, *args, **kwargs):
        object =Memo.objects.filter(user_id__id__exact = self.request.user.id)
        return object

# Memoの作成機能
class MemoCreateView(LoginRequiredMixin,generic.CreateView):
    model = Memo
    form_class = MemoForm

    #フォーム送信者をログインユーザーIDに自動設定
    def form_valid(self, form):
        form.instance.user_id = self.request.user
        form.instance.status = '未達成'
        return super(MemoCreateView, self).form_valid(form)

    #メモを新規作成(文字カウントのため自作)
    def create_memo(self,request,pk):
        memo = get_object_or_404(Memo, pk=pk)

        if request.method == 'POST':
            problem = request.POST['problem']
            solution = request.POST['solution']
            Memo.objects.create(
                problem=problem,
                solution=solution,
            )
            return redirect('memo:list') 
        return redirect('memo:list')
    success_url = reverse_lazy('memo:list')

    
    
# Memoの編集機能
class MemoUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = Memo
    form_class = MemoForm
    
    #自分のメモしか編集できないようにフィルター
    def get_queryset(self, *args, **kwargs):
        object =Memo.objects.filter(user_id__id__exact = self.request.user.id)
        return object

    success_url = reverse_lazy('memo:list')

# Memoの削除機能
class MemoDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = Memo
    success_url = reverse_lazy('memo:list')

#submemo complete
@login_required
def subcomplete(request):
    template = loader.get_template('memo/memo_subcomplete.html')
    context = { }
    return render(request, 'memo/memo_subcomplete.html', context)
    
# Memoの作成機能
class MemoSUBCreateView(LoginRequiredMixin,generic.CreateView):
    model = Memo
    template_name="memo/memo_subform.html"
    form_class = MemoForm

    #フォーム送信者をログインユーザーIDに自動設定
    def form_valid(self, form):
        form.instance.user_id = self.request.user
        form.instance.status = '未達成'
        return super(MemoSUBCreateView, self).form_valid(form)

    #メモを新規作成(文字カウントのため自作)
    def create_memo(self,request,pk):
        memo = get_object_or_404(Memo, pk=pk)

        if request.method == 'POST':
            problem = request.POST['problem']
            solution = request.POST['solution']
            Memo.objects.create(
                problem=problem,
                solution=solution,
            )
            return redirect('memo:subcomplete') 
        return redirect('memo:subcomplete')
    success_url = reverse_lazy('memo:subcomplete')
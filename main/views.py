from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import TextComment, Location, Money, OrderBill
from .forms import TextCommentForm, LocationForm
import random


def main(request):
    if request.method == 'POST':
        return render(request, "main.html", {
            'comments': TextComment.objects.filter(author=request.user),
            'comment_form': TextCommentForm(),
        })
    else:
        return render(request, "main.html", {
            'comment_form': TextCommentForm(),
        })

# def text_comment(request):
#     if request.method == 'POST':
#         form = TextCommentForm(request.POST)
#         if form.is_valid():
#             print('form valid-comments')
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.message_response = 'nice to meet you'
#             comment.save()
#         return render(request, 'main.html',{
#             'comments' : TextComment.objects.filter(author=request.user),
#             'comment_form': TextCommentForm(),
#         })
#     return redirect('main:main')


def text_comment(request):
    if request.method == 'POST':
        form = TextCommentForm(request.POST)
        if form.is_valid():
            print('form valid-comments')
            comment = form.save(commit=False)
            comment.author = request.user
            if '안녕' in comment.message:
                comment.message_response = '앗 나도 반가워'
            elif '잘가' in comment.message:
                comment.message_response = '헉.. 잘가...'
            elif '오랜만' in comment.message:
                comment.message_response = '응 맞아 오랜만이야!'
            elif '집' in comment.message:
                location = Location.objects.filter(author=request.user)
                comment.message_response = '집의 위치 입니다.'
            else:
                comment.message_response = '준비 중입니다~'
            comment.save()
        return render(request, 'main.html', {
            'comments': TextComment.objects.filter(author=request.user),
            'comment_form': TextCommentForm(),
            # 'location' : location,
        })
    return redirect('main:main')


def chat_comment(request):
    if request.method == 'POST':
        form = TextCommentForm(request.POST)
        if request.session['time'] == 'am8':
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                # 좋은 아침이에요에 대한 대답
                if 'am8' not in request.session.keys():
                    if any(x in comment.message for x in ['응', '그래', '어', '좋아', '그럴까']):
                        comment.message_response = '넵'
                        location = Location.objects.get(title='회사')
                        comment.location = location
                        request.session['am8'] = 1
                        request.session['order'] = 'start'
                        comment.save()
                        TextComment.objects.create(author=request.user, message_response='미리 장을 봐둘까요?', message='')
                        return render(request, 'main/chat_detail.html', {
                            'comments': TextComment.objects.filter(author=request.user),
                            'comment_form': TextCommentForm(),
                            'money': Money.objects.latest('pk').money,
                            })

                ## 로케이션 지정 안 할때 알고리즘 필요함.

                # elif request.session['am8'] == 0:
                #     #comment.message_response = '미리 장을 봐둘까요??'
                #     request.session['am8'] = 1
                #     request.session['order'] = 'start'
                #     comment.save()
                # 장볼거야?에 대한 대답
                elif request.session['am8'] == 1:
                    if request.session['order'] == 'start':
                        if any(x in comment.message for x in ['응', '그래', '어', '좋아', '그럴까']):
                            comment.message_response = '어떤 식료품을 주문할까요?'
                            request.session['am8'] = 1
                            request.session['order'] = 'start'
                            comment.save()
                        elif '주문' in comment.message:
                            pre_pro = comment.message
                            pre_pro= pre_pro.split(",")
                            order_list = []
                            order_bill = OrderBill.objects.latest('pk')
                            for x in pre_pro :
                                if '마늘' in x :
                                    order_bill.order_bill += 1500
                                    order_list.append('마늘,')
                                elif '양파' in x :
                                    order_bill.order_bill += 2000
                                    order_list.append('양파,')
                                elif '삼겹살' in x :
                                    order_bill.order_bill += 10000
                                    order_list.append('삼겹살,')
                                else :
                                    order_list += ', 등록되지 않은 상품'
                            comment.save()
                            order_bill.save()
                            request.session['am8'] = 1
                            request.session['order'] = 'ing'
                            order_list += '(을)를 주문하겠습니다. 총 가격은 {0} 입니다'.format(order_bill.order_bill)
                            order_list_str = " ".join(str(x) for x in order_list)
                            TextComment.objects.create(author=request.user, message_response=order_list_str, message='')
                    elif request.session['order'] == 'ing':
                        if any(x in comment.message for x in ['응', '그래', '어', '좋아']):
                            money = Money.objects.latest('pk')
                            order_bill = OrderBill.objects.latest('pk')
                            money.money -= order_bill.order_bill
                            order_bill.order_bill = 0
                            order_bill.save()
                            money.save()
                            request.session['order'] = 'end'
                            request.session['am8'] = 2
                            comment.save()
                        else :
                            request.session['order'] = 'end'
                            request.session['am8'] = 2
                            comment.save()

                    # comment.message_response = '네 알겠습니다.'
                    # request.session['am8'] = 2
                    # comment.save()
                    #TextComment.objects.create(author=request.user, message_response='스타벅스로 갈까요?', message='')
                # 스벅 고?에 대한 대답
                # elif request.session['am8'] == 2:
                #     if any(x in comment.message for x in ['응', '그래', '어', '좋아']):
                #         comment.message_response = '스타벅스로 목적지를 설정합니다~'
                #     else:  # 스벅안가기로함
                #         comment.message_response = '네 알겠습니다.'
                #     comment.save()

        elif request.session['time'] == 'pm6':
            form = TextCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                if any(x in comment.message for x in ['좋았', '좋은' ,'행복']):
                    random_msg = ['오~ 오늘의 하루는 별이 다섯개?!', '룰루~ ㅎㅎ 뭐 때문에 좋았어요', '으와~ 나이스입니다 ㅎㅎ']
                    comment.message_response = random.choice(random_msg)
                else:
                    random_msg = ['허걱.. 힘내세요ㅠㅠ..', '앗, 그러면 신나는 음악이라도 틀어드릴게요ㅎㅎ!', '아 이럴 땐 돈 쓰러 가야하는데~']
                    comment.message_response = random.choice(random_msg)
                comment.save()

        elif request.session['time'] == 'sbuck':
            form = TextCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                # 아이스, 차가운이라는 단어와 아메리카노라는 단어가 둘다 있을 경우에
                if 'sbuck' not in request.session.keys():
                    if all(x in comment.message for x in ['아이스', '아메리카노']) or all(x in comment.message for x in ['차가운', '아메리카노']):
                        comment.message_response = '아이스 아메리카노를 주문합니다. 사이즈는 어떻게 할까요?'
                        request.session['sbuck'] = 'americano'
                        request.session['order'] = 'start'
                        comment.save()
                    # 아이스라는 단어는 없는데 아메리카노가 있을때
                    elif '프라푸치노' in comment.message:
                        comment.message_response = '프라푸치노를 주문합니다. 사이즈는 어떻게 할까요?'
                        request.session['sbuck'] = 'frappuccino'
                        request.session['order'] = 'start'
                        comment.save()
                    else:
                        request.session['sbuck'] = 'not selected'
                elif request.session['order'] == 'start' :
                    if request.session['sbuck'] == 'americano':
                        order_bill = OrderBill.objects.latest('pk')
                        if any(x in comment.message for x in ['tall', '톨']):
                            comment.message_response = '아이스 아메리카노 톨 사이즈로 주문할까요? 4100원입니다.'
                            order_bill.order_bill += 4100
                        elif any(x in comment.message for x in ['grande', '그란데']):
                            comment.message_response = '아이스 아메리카노 그란데 사이즈로 주문할까요? 4600원입니다.'
                            order_bill.order_bill += 4600
                        request.session['order'] = 'ing'
                        order_bill.save()
                        comment.save()
                    elif request.session['sbuck'] == 'frappuccino':
                        order_bill = OrderBill.objects.latest('pk')
                        if any(x in comment.message for x in ['tall', '톨']):
                            comment.message_response = '프라푸치노 톨 사이즈로 주문할까요? 5600원입니다.'
                            order_bill.order_bill += 5600
                        elif any(x in comment.message for x in ['grande', '그란데']):
                            comment.message_response = '아이스 아메리카노 그란데 사이즈로 주문할까요? 6100원입니다.'
                            order_bill.order_bill += 6100
                        request.session['order'] = 'ing'
                        order_bill.save()
                        comment.save()
                elif request.session['order'] == 'ing':
                        if any(x in comment.message for x in ['응', '그래', '어', '좋아', '그럴까']):
                            money = Money.objects.latest('pk')
                            order_bill = OrderBill.objects.latest('pk')
                            money.money -= order_bill.order_bill
                            money.save()
                            order_bill.order_bill = 0
                            order_bill.save()
                            comment.save()
                            request.session['order'] = 'end'
            else:
                    TextComment.objects.create(author=request.user, message_response='메뉴는 아이스 아메리카노, 프라푸치노 중에서 선택 가능합니다.', message=comment.message)
                    del request.session['sbuck']

        return render(request, 'main/chat_detail.html', {
            'comments': TextComment.objects.filter(author=request.user),
            'comment_form': TextCommentForm(),
            'money': Money.objects.latest('pk').money,
        })
    return redirect('main:chat')


def location_list(request):
    return render(request, 'main/location_list.html', {
        'location_list': Location.objects.all(),
    })


def chat(request):
    if request.method == 'POST':
        v1 = request.POST.get('time_')
        request.session['time'] = v1
        if v1 == 'am8':
            TextComment.objects.create(author=request.user, message_response='좋은 아침이에요, 회사로 경로를 설정할까요?', message='')
        elif v1 == 'pm6':
            TextComment.objects.create(author=request.user, message_response='오늘은 어땠나요?', message='')
        elif v1 == 'sbuck':
            TextComment.objects.create(author=request.user, message_response='스타벅스로 주문을 합니다. 어떤 것을 주문할까요?', message='')
        return render(request, 'main/chat.html', {
            'comments': TextComment.objects.filter(author=request.user),
            'comment_form': TextCommentForm(),
            'money': Money.objects.latest('pk').money
            # 'location' : location,
        })
    return render(request, 'main/chat.html', {
        'money': Money.objects.latest('pk').money
    })


def flush(request):
    if request.method == 'POST' and 'time' in request.session.keys():
        # request.session.flush()
        if 'time' in request.session.keys():
            del request.session['time']
        if 'am8' in request.session.keys():
            del request.session['am8']
        if 'pm6' in request.session.keys():
            del request.session['pm6']
        if 'sbuck' in request.session.keys():
            del request.session['sbuck']

        txtcomment = TextComment.objects.all()
        if txtcomment:
            txtcomment.delete()

    return redirect('main:chat')
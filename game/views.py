from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from .models import ImageGame, UsedImageByUser, UserStatistics
from datetime import datetime, timedelta


def get_today_image():
    today_date = datetime.now() - timedelta(days=0)
    today_date = today_date.date()
    game_ = ImageGame.objects.filter(is_image_used=True, used_at=today_date).last()
    if not game_:
        game_ = ImageGame.objects.filter(is_image_used=False).order_by('id').first()
        if game_:
            game_.is_image_used = True
            game_.used_at = datetime.now().date()
            game_.save()
    return game_


def check_image_against_user(game_, user_):
    uibu = UsedImageByUser.objects.filter(image=game_, user=user_).last()
    if not uibu:
        uibu = UsedImageByUser.objects.create(image=game_, user=user_, attempt_no=0,
                                              pixelation_level=game_.pixelation_level)
    return uibu


def get_remaining_time_in_game():
    now = datetime.now()
    next_day_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    remaining_time = next_day_midnight - now
    remaining_time = remaining_time.total_seconds()
    return remaining_time


def get_all_titles_of_games_for_guesses():
    games_ = ImageGame.objects.filter(is_image_used=True).all()
    return games_


def change_stats_of_existing_game_against_user(today_game_stats, user_guess):
    today_game_stats.attempt_no = today_game_stats.attempt_no + 1
    if today_game_stats.attempts_history:
        today_game_stats.attempts_history = today_game_stats.attempts_history + ',' + user_guess
    else:
        today_game_stats.attempts_history = user_guess
    today_game_stats.pixelation_level = today_game_stats.pixelation_level - 1

    if user_guess.lower().strip() == today_game_stats.image.title.lower().strip():
        today_game_stats.is_user_win = True
        today_game_stats.is_attempt_done = True

    if today_game_stats.attempt_no == 5:
        today_game_stats.is_attempt_done = True
    today_game_stats.save()
    return today_game_stats


def get_attempts_left(user_stats):
    attempt_no = user_stats.attempt_no
    attempts_left = 5 - attempt_no
    return attempts_left


def get_stats_to_show_in_home_title_against_game(user_stats):
    total_attempts = user_stats.attempt_no
    if not user_stats.is_attempt_done:
        return None

    att = user_stats.attempts_history.split(',')
    dict_ = {
        'total_attempts': total_attempts,
        'attempts_history': user_stats.attempts_history,
        'is_user_win': user_stats.is_user_win,
        'attempts': att
    }
    return dict_


def index(request):
    remaining_time = get_remaining_time_in_game()
    game_image_ = get_today_image()
    total_games = get_all_titles_of_games_for_guesses()
    context = {'game': game_image_, 'games': total_games, 'user_stats': None,
               'game_guessed': False, 'attempts_left': 0, 'result': None,
               'pixelation_level': 0, 'is_attempt_done': False,
               'remaining_time': remaining_time}

    if not game_image_:
        return render(request, 'index.html', context=context)

    context['pixelation_level'] = game_image_.pixelation_level

    if request.user.is_authenticated:
        today_game_stats = check_image_against_user(game_image_, request.user)
        context['attempts_left'] = get_attempts_left(today_game_stats)
        context['pixelation_level'] = today_game_stats.pixelation_level
        context['is_attempt_done'] = today_game_stats.is_attempt_done
        context['user_stats'] = today_game_stats
        context['result'] = get_stats_to_show_in_home_title_against_game(today_game_stats)
        return render(request, 'index.html', context=context)

    return render(request, 'index.html', context=context)


@login_required
def guess(request):
    image_id = request.POST['image_id']
    user_guess = request.POST['guess']
    game = ImageGame.objects.filter(id=image_id).last()

    correct_title = game.title.lower()
    user_guess_lower = user_guess.lower()
    today_game_stats = check_image_against_user(game, request.user)
    today_game_stats = change_stats_of_existing_game_against_user(today_game_stats, user_guess)

    if user_guess_lower == correct_title:
        update_statistics(request.user, True)
    else:
        if today_game_stats.attempt_no == 5:
            update_statistics(request.user, False)

    if today_game_stats.attempt_no == 5:
        return redirect('statistics')
    return redirect('index')


def update_statistics(user, is_win):
    user_stats = UserStatistics.objects.get_or_create(user=user)[0]
    user_stats.played_matches += 1
    if is_win:
        user_stats.win_count += 1
        user_stats.current_streak += 1
        user_stats.max_streak = max(user_stats.max_streak, user_stats.current_streak)
    else:
        user_stats.current_streak = 0
    user_stats.save()


def get_user_statistics(user):
    return UserStatistics.objects.get_or_create(user=user)[0]


def logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')


@login_required
def statistics(request):
    user_stats = UserStatistics.objects.get_or_create(user=request.user)[0]
    return render(request, 'result.html', {'user_stats': user_stats})

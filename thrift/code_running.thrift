namespace cpp code_running_service

struct Bot {
    1: i32 userId,
    2: string botCode,
    3: string input,
}

service CodeRunning {

    i32 add_bot_code(1: Bot bot, 2: string info);
}

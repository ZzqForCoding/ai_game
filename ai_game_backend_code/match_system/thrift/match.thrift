namespace py match_service

struct Player {
    1: i32 id,
    2: string username,
    3: string photo,
    4: i32 rating,
    5: string channel_name,
    6: i32 operate,
    7: i32 bot_id,
    8: i32 game_id,
}

service Match {

    i32 add_player(1: Player player),

    i32 remove_player(1: Player player),
}

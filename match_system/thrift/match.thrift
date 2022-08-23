namespace cpp match_service

struct Player {
    1: i32 id,
    2: string username,
    3: string photo,
    4: i32 rating,
    5: string channel_name,
}

service Match {

    i32 add_player(1: Player player, 2: string info),

    i32 remove_player(1: Player player, 2: string info),
}

namespace py code_running_service

service CodeRunning {

    i32 start_container(1: string uuid, 2: string code, 3: string lang);

    i32 stop_container(1: string uuid);

    string compile(1: string uuid);

    i32 prepare_data(1: string uuid, 2:string data);

    string run(1: string uuid);
}

struct User {
    1: i64 id,
    2: optional string password,
    3: optional byte state,
    4: optional string create_time,
    5: optional string update_time,
}


service UserService {
    string ping(),
    void createUser(1: User user),
}

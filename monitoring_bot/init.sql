create type status as enum ('member', 'banned', 'left', 'admin', 'not_a_member');

create table users
(
    user_id bigint not null primary key,
    username text not null,
    enter_date timestamp not null,
    leave_date timestamp,
    status status not null,
    has_chat_with_bot boolean default false not null
);

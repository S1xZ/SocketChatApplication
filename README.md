# Message format Chat App 👩‍💻

- [ ] The client can set a nickname.

- [ ] Each client can see a list of all clients.

- [ ] Each client can see a list of all created chat groups

```json
// Send to backend
{
    "type":"username"
    "data": {USERNAME}
}
// Receive
{
    "type": "users",
    "isExist": False,
    "data": {LIST_OF_USERS}
}

{
    "type": "groups",
    "data": {LIST_OF_GROUPS}
}
// Receive (id Username already exist)
{
    "type": "users",
    "isExist": True,
    "data": []
}
```

---

- [ ] Each client can create a chat group(s)

- [ ] Each client can see a list of all created chat groups

```json
// Send to backend
{
"type":"create"
"data": {GROUPNAME}
}
// Receive
{
"type": "groups",
"isExist": {isExist},
"isJoin": {isJoin},
"data": {LIST_OF_GROUPS}
}
```

---

- [ ] Each client can join a chat group(s)

- [ ] Each client can see a list of all created chat groups

```json
// Send to backend
{
"type":"join"
"data": {GROUPNAME}
}
// Receive
{
"type": "groups",
"isExist": {isExist},
"isJoin": {isJoin},
"data": {LIST_OF_GROUPS}
}
```

---

- [ ] Each client can send a group message.

```json
// Send to backend
{
"type": "group_message"
"group": {GROUP_NAME},
"data": {MESSAGE}
}
// Receive (For user in group minus sender only)
{
"type": "group_message",
"group": {GROUP_NAME},
"sender": {SENDER_USERNAME},
"data": {MESSAGE}
}
```

- [ ] Each client can send a direct message to other clients in the list.

```json
// Send to backend
{
"type": "direct_message",
"recipient": {RECIPENT_NAME},
"data": {MESSAGE}
}
```

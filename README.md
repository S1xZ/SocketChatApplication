# Message format Chat App 👩‍💻

- [x] The client can set a nickname.

- [ ] Each client can see a list of all clients.

```json
// Send Create username
{
    "type":"username"
    "data": {USERNAME}
}
// Receive (id Username not exist)
{
    "type": "users",
    "data": {LIST_OF_USERS}
}
// Receive (id Username already exist)
{
    "type": "users",
    "isExist": true
}
```

---

- [x] Each client can create a chat group(s)

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

- [x] Each client can join a chat group(s)

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

- [x] Each client can send a group message.

```json
// Send to backend
{
"type": "group_message"
"group": {GROUP_NAME},
"data": {MESSAGE}
}
// Receive (For user in group exclude sender)
{
"type": "group_message",
"group": {GROUP_NAME},
"sender": {SENDER_USERNAME},
"data": {MESSAGE}
}
```

---

- [x] Each client can send a direct message to other clients in the list.

```json
// Send Message to server
{
"type": "direct_message",
"recipient": {RECIPENT_NAME},
"data": {MESSAGE}
}
// Receive (For username in recipient)
{
"type": "direct_message",
"sender": {RECIPENT_NAME},
"data": {MESSAGE}
}
```

---

- [x] The system must have at least 2 computers for implementing the chat application,
      one for the server and client and others for the client
- [ ] The chat room must have a chat box and a chat window.

- [ ] In a group chat room, each client must see all the text messages from other clients
      in that chat group

---

## More Functional Requirements (1.0 points per feature)

1. The
2. The
3. The
4. The

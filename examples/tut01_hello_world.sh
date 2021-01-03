curl -v -d '{"email":"a@b.com","password":"xyz"}' \
     -H "Content-Type: application/json" http://localhost:5000/user

#< HTTP/1.0 200 OK
#< Content-Type: application/json
#< Content-Length: 45
#<
#{
#  "_id": "a@b.com",
#  "password": "xyz"
#}


curl -v http://localhost:5000/users
#< HTTP/1.0 200 OK
#< Content-Type: application/json
#< Content-Length: 57
#<
#[
#  {
#    "_id": "a@b.com",
#    "password": "xyz"
#  }
#]


curl -v http://localhost:5000/user/a@b.com
#< HTTP/1.0 200 OK
#< Content-Type: application/json
#< Content-Length: 45
#<
#{
#  "_id": "a@b.com",
#  "password": "xyz"
#}


curl -v -X PUT -d '{"password":"new_pass"}' \
    -H "Content-Type: application/json" http://localhost:5000/user/a@b.com
#< HTTP/1.0 200 OK
#< Content-Type: application/json
#< Content-Length: 50
#<
#{
#  "_id": "a@b.com",
#  "password": "new_pass"
#}


curl -v -X DELETE http://localhost:5000/user/a@b.com
#< HTTP/1.0 200 OK
#< Content-Type: application/json
#< Content-Length: 45
#<
#{
#  "_id": "a@b.com",
#  "password": "xyz"
#}

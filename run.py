from app.data import api, app, users_resource


def main():
    api.add_resource(users_resource.UserResource, '/api/users/<int:user_id>')
    api.add_resource(users_resource.UsersListResource, '/api/users')
    app.run()


if __name__ == '__main__':
    main()

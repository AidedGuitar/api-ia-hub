export interface UserInterface {
	id: string;
	use_name: string;
	use_email: string;
	use_career: string;
	use_academic_level: string;
	use_rol_id: string;
}

export default class UserServices {
	constructor() {}

	public async getUserByEmail(
		use_email: string
	): Promise<UserInterface | string> {
		const config = {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
			credentials: "include" as RequestCredentials,
		};

		const response = await fetch(
			`${process.env.NEXT_PUBLIC_AUTH_URL}/users`,
			config
		);

		const data = await response.json();

		if (!response.ok) {
			throw new Error(data.message);
		}

		if (Object.keys(data).length === 0) {
			return "NOT_FOUND";
		}

        const user = data.find((user: UserInterface) => user.use_email === use_email);

        if (!user) {
            return "NOT_FOUND";
        }

		return user;
	}
}

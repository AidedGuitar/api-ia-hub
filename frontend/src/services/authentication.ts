interface responseLogin {
	status: number;
}

interface responseRegister {
	id: string;
	use_name: string;
	use_email: string;
	use_career: string;
	use_academic_level: string;
	use_rol_id: string;
	detail?: string;
	status: number;
}

export default class AuthenticationServices {
	constructor() {}

	public async postLogin(data: {
		use_email: string;
		password: string;
	}): Promise<responseLogin> {
		const response = await fetch("/api/login", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(data),
		});

		if (response.ok) {
			return { status: response.status };
		}

		return { status: response.status };
	}

	public async postRegister(data: {
		use_name: string;
		use_email: string;
		password: string;
		use_career: string;
		use_academic_level: string;
	}): Promise<responseRegister> {
		const config = {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(data),
		};

		const response = await fetch(
			`${process.env.NEXT_PUBLIC_AUTH_URL}/auth/register`,
			config
		);

		if (response.ok) {
			const res = await response.json();

			return {
				id: res.id,
				use_name: res.use_name,
				use_email: res.use_email,
				use_career: res.use_career,
				use_academic_level: res.use_academic_level,
				use_rol_id: res.use_rol_id,
				status: response.status,
			};
		}

		return {
			id: "",
			use_name: "",
			use_email: "",
			use_career: "",
			use_academic_level: "",
			use_rol_id: "",
			status: response.status,
		};
	}

	public async postLogout() {
		const config = {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
		};

		const response = await fetch(
			`${process.env.NEXT_PUBLIC_AUTH_URL}/auth/logout`,
			config
		);

		if (!response.ok) {
			throw new Error(response.status.toString());
		}

		return response.status;
	}
}

import { ApplicationInterface } from "@/app/page";

export default class ApplicationServices {
	public async getApplications(): Promise<ApplicationInterface[]> {
		const config = {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
			credentials: "include" as RequestCredentials,
		};

		const response = await fetch(
			`${process.env.NEXT_PUBLIC_AUTH_URL}/apps`,
			config
		);

		const data = await response.json();

		if (!response.ok) {
			throw new Error(data.message);
		}

		return data;
	}

	public async getApplicationById(
		idApplication: string
	): Promise<ApplicationInterface> {
		const config = {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
			credentials: "include" as RequestCredentials,
		};

		const response = await fetch(
			`${process.env.NEXT_PUBLIC_AUTH_URL}/apps/${idApplication}`,
			config
		);

		const data = await response.json();

		if (!response.ok) {
			throw new Error(data.message);
		}

		return data;
	}

	public async recommendationApplications(): Promise<ApplicationInterface[]> {
		const config = {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
			credentials: "include" as RequestCredentials,
		};

		try {
			const response = await fetch(
				`${process.env.NEXT_PUBLIC_AUTH_URL}/recommendations`,
				config
			);
			const data = await response.json();

			if (!response.ok) {
				throw new Error(data.message);
			}

			return data;
		} catch (error) {
			console.log("error", error);
		}

		return [];
	}

	public async detailApplication(
		idApplication: string
	): Promise<ApplicationInterface | string> {
		const config = {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
			credentials: "include" as RequestCredentials,
		};

		const response = await fetch(
			`${process.env.NEXT_PUBLIC_AUTH_URL}/apps/${idApplication}`,
			config
		);

		const data = await response.json();

		if (response.status === 404) {
			return "NOT_FOUND";
		}

		if (!response.ok) {
			throw new Error(data.message);
		}

		return data;
	}
}

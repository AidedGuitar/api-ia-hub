import { UserInterface } from "./user";

export interface FeedbackInterface {
	user_id: string;
	user: UserInterface;
	application_id: string;
	fee_rating: number;
	fee_comment: string;
	fee_date: string;
	id: string;
	created_at: string;
	updated_at: string;
}

export interface FeedbackCreateInterface {
	user_id: string;
	application_id: string;
	fee_rating: number;
	fee_comment: string;
	fee_date: string;
}

export default class FeedbackServices {
	constructor() {}

	public async getFeedbacksByIdApplication(
		idApplication: string
	): Promise<FeedbackInterface[] | string> {
		const config = {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
			credentials: "include" as RequestCredentials,
		};

		const response = await fetch(
			`${process.env.NEXT_PUBLIC_AUTH_URL}/feedback?application_id=${idApplication}`,
			config
		);

		const data = await response.json();

		if (!response.ok) {
			throw new Error(data.message);
		}

		if (data.length === 0) {
			return "NOT_FOUND";
		}

		return data;
	}

	public async createFeedback(data: FeedbackCreateInterface) {
		const config = {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(data),
			credentials: "include" as RequestCredentials,
		};

		const response = await fetch(
			`${process.env.NEXT_PUBLIC_AUTH_URL}/feedback`,
			config
		);

		if (!response.ok) {
			throw new Error(response.status.toString());
		}

		return { status: response.status, data: await response.json() };
	}
}

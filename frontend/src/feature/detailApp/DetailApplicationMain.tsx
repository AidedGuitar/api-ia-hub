"use client";

import { ApplicationInterface } from "@/app/page";
import ApplicationServices from "@/services/application";
import FeedbackServices, { FeedbackInterface } from "@/services/feedback";
import UserServices, { UserInterface } from "@/services/user";
import { useEffect, useState } from "react";
import FormFeedback from "./FormFeedback";
import { ImageIcon, StarIcon } from "@/assets";

export default function DetailApplicationMain({
	idApplication,
}: {
	idApplication: string;
}) {
	const [dataApplication, setDataApplication] = useState<
		ApplicationInterface | string
	>({} as ApplicationInterface);

	const [dataFeedback, setDataFeedback] = useState<
		FeedbackInterface[] | string
	>([]);
	const [dataUser, setDataUser] = useState<UserInterface | string>(
		{} as UserInterface
	);

	const applicationServices = new ApplicationServices();
	const feedbackServices = new FeedbackServices();
	const userServices = new UserServices();

	async function fetchDetailApplication(idApplication: string) {
		const data = await applicationServices.detailApplication(idApplication);

		setDataApplication(data);
	}

	async function fetchFeedbacks(idApplication: string) {
		const data = await feedbackServices.getFeedbacksByIdApplication(
			idApplication
		);

		setDataFeedback(data);
	}

	async function getIdUser() {
		const response = await fetch("/api/login", { method: "GET" });

		const data = await response.json();

		if (!response.ok) {
			throw new Error(data.message);
		}

		const dataUser = await userServices.getUserByEmail(data.sub);

		setDataUser(dataUser);
	}

	const refreshDataFeedback = () => fetchFeedbacks(idApplication);

	useEffect(() => {
		Promise.all([
			fetchDetailApplication(idApplication),
			fetchFeedbacks(idApplication),
			getIdUser(),
		]);
	}, []);

	const handlerFormatDate = (date: string) => {
		const dateObj = new Date(date);

		const formateada = dateObj.toLocaleDateString("es-CO");

		return formateada;
	};

	return (
		<main className="p-8 max-w-[1024px] mx-auto flex flex-col gap-8">
			{Object.keys(dataApplication).length > 0 ? (
				typeof dataApplication === "string" ? (
					<p>{dataApplication}</p>
				) : (
					<section className="flex gap-10 rounded-md justify-between h-fit">
						<div className="relative p-2 justify-items-center bg-edtech-blue-100 w-full min-h-full rounded-lg">
							<ImageIcon className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64" />
						</div>
						<div className="w-full flex flex-col gap-5">
							<div className="flex justify-between">
								<h1 className="text-2xl font-bold">
									{dataApplication.app_name}
								</h1>
								<div className="text-2xl flex items-center gap-px">
									<p>
										{Number(
											dataApplication.avg_rating
										).toFixed(1)}
									</p>
									<StarIcon className="w-8 h-8 fill-amber-200" />
								</div>
							</div>

							<div className="flex flex-col text-lg">
								<span className="font-medium">Categoria: </span>
								<p className="text-base text-neutral-700 px-3 py-1 rounded-full border border-neutral-700 bg-neutral-300 w-fit">
									{dataApplication.app_category}
								</p>
							</div>

							<div className="flex flex-col text-lg">
								<span className="font-medium">
									Descripción:{" "}
								</span>
								<p className="text-base text-neutral-700">
									{dataApplication.app_description}
								</p>
							</div>

							<div className="flex flex-col text-lg">
								<span className="font-medium">
									Palabras clave:{" "}
								</span>
								<p className="text-base text-neutral-400">
									{dataApplication.app_keywords}
								</p>
							</div>
						</div>
					</section>
				)
			) : (
				<h1>Loading</h1>
			)}

			{/* --- FEEDBACKS --- */}
			<section className="flex flex-col gap-4">
				<h2 className="text-xl font-semibold">Comentarios</h2>

				{Object.keys(dataUser).length > 0 &&
					typeof dataUser === "object" && (
						<FormFeedback
							idApplication={idApplication}
							idUser={dataUser.id}
							refreshDataFeedback={refreshDataFeedback}
						/>
					)}

				{dataFeedback.length > 0 ? (
					<div className="flex flex-col gap-5 border-t border-t-neutral-300 pt-5">
						{typeof dataFeedback === "string" ? (
							<p>No hay resultados</p>
						) : (
							dataFeedback.map((item, index) => (
								<div
									key={index}
									className={
										index % 2 === 0
											? "bg-edtech-acent-100 border rounded-md p-2"
											: "border rounded-md p-2 flex flex-col gap-3"
									}>
									<div className="flex justify-between">
										<span className="text-lg font-semibold">
											{item.user.use_name}
										</span>
										<div className="flex gap-1 items-center">
											<p>
												{Number(
													item.fee_rating
												).toFixed(1)}
											</p>
											<StarIcon className="w-5 h-5 fill-amber-200" />
										</div>
									</div>
									<div className="flex justify-between items-end">
										<p>{item.fee_comment}</p>
										<p>
											{handlerFormatDate(item.fee_date)}
										</p>
									</div>
								</div>
							))
						)}
					</div>
				) : (
					<h1>Loading</h1>
				)}
			</section>
		</main>
	);
}

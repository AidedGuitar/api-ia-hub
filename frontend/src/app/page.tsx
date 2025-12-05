"use client";

import AppCard from "@/components/AppCard";
import ApplicationServices from "@/services/application";
import { useEffect, useState } from "react";

export interface ApplicationInterface {
	id: string;
	app_name: string;
	app_category: string;
	app_link: string;
	app_description: string;
	app_source: string;
	app_keywords: string;
	app_academic_level: string;
	avg_rating: number;
	created_at: string;
	updated_at: string;
}

export default function Home() {
	const [apps, setApps] = useState<ApplicationInterface[]>([]);
	const [recommendations, setRecommendations] = useState<
		ApplicationInterface[]
	>([]);

	const applicationServices = new ApplicationServices();

	async function fetchApps() {
		const data = await applicationServices.getApplications();

		setApps(data);
	}

	async function fetchRecommendation() {
		const data = await applicationServices.recommendationApplications();

		setRecommendations(data);
	}

	useEffect(() => {
		Promise.all([fetchRecommendation(), fetchApps()]);
	}, []);

	return (
		<main className="p-8 max-w-[1024px] mx-auto">
			<section>
				<h1 className="text-2xl font-bold mb-4 text-edtech-blue">
					Aplicaciones recomendadas
				</h1>
				<div className="flex flex-wrap gap-4 justify-between">
					{recommendations.map((recommendation) => (
						<AppCard key={recommendation.id} {...recommendation} />
					))}
				</div>
			</section>

			<section className="pt-12">
				<h2 className="text-2xl font-bold mb-4 text-edtech-blue">
					Lista de Aplicaciones
				</h2>
				<div className="flex flex-wrap gap-4 justify-between">
					{apps.map((app) => (
						<AppCard key={app.id} {...app} />
					))}
				</div>
			</section>
		</main>
	);
}

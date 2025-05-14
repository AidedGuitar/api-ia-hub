"use client";

import { useEffect, useState } from "react";
import axios from "axios";

type App = {
	id: number;
	name: string;
	category: string;
};

export default function Home() {
	const [apps, setApps] = useState<App[]>([]);

	useEffect(() => {
		axios
			.get("http://localhost:8000/recommendations?user_id=1")
			.then((response) => {
				setApps(response.data.recommendations);
			})
			.catch((error) => console.error(error));
	}, []);

	return (
		<main className="p-8">
			<h1 className="text-2xl font-bold mb-4 text-emerald-500">Recomendaciones de Apps</h1>
			<h1 className="text-2xl font-bold mb-4 text-[#10b981]">Recomendaciones de Apds</h1>
			<ul className="space-y-2">
				{apps.map((app) => (
					<li key={app.id} className="border p-4 rounded">
						<strong>{app.name}</strong> - {app.category}
					</li>
				))}
			</ul>
		</main>
	);
}

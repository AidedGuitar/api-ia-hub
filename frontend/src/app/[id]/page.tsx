import DetailApplicationMain from "@/feature/detailApp/DetailApplicationMain";
import { Metadata } from "next";

interface PageProps {
	readonly params: Promise<{
		id: string;
	}>;
}

export const metadata: Metadata = {
	title: "Detalle de la aplicación",
};

export default async function page({ params }: PageProps) {
	const { id } = await params;

	return <DetailApplicationMain idApplication={id} />;
}

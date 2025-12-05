import LoginMain from "@/feature/login/LoginMain";
import { Metadata } from "next";

export const metadata: Metadata = {
	title: "Inicio de sesión",
	description:
		"Ingreso a la plataforma de Ecosistemas de IA de la U. Libre seccional Cali",
};

export default function Login() {
	return (
		<div className="flex p-5 md:p-10 bg-linear-to-r from-edtech-blue-300 to-edtech-blue-900 h-svh md:h-screen md:items-center justify-center bg-gray-100">
			<LoginMain />
		</div>
	);
}

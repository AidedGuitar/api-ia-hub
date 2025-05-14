import LoginMain from "@/feature/login/LoginMain";
import { Metadata } from "next";

export const metadata: Metadata = {
	title: "Inicio de sesión",
	description:
		"Ingreso a la plataforma de Ecosistemas de IA de la U. Libre seccional Cali",
};

export default function Login() {
	return (
		<div className="flex p-10 bg-linear-to-r from-bismark-200 to-bismark-600 min-h-screen items-center justify-center">
			<LoginMain />
		</div>
	);
}

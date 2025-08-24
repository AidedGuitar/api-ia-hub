"use client";

import { GoogleIcon } from "@/assets/socialIcon";
import { signIn } from "next-auth/react";
import Image from "next/image";
import LoginForm from "./LoginForm";

function LoginMain() {
	const handleSingInGoogle = () => {
		signIn("google", { callbackUrl: "/" });
	}

	return (
		<section className="flex bg-edtech-blue-100 rounded-md md:h-full w-full p-5 md:p-10 gap-5 lg:gap-10 max-w-[1440px] h-[100hv]">
			<div className="bg-white overflow-y-auto flex flex-col h-full gap-2.5 md:gap-5  w-full lg:w-1/2 rounded-md px-5 py-3 md:p-5 shadow-2xl items-center md:pb-10">
				<Image
					src="/logo.webp"
					alt="Edtech avance con IA"
					width={669}
					height={669}
					className="h-24 lg:h-[7rem] w-24 lg:w-[7rem] object-center"
				/>
				<div className="flex flex-col gap-3 w-full">
					<h1 className="text-3xl font-bold">Inicio de sesión</h1>
					<p className="text-base">
						¿Aún no tiene una cuenta?{" "}
						<a href="" className="text-bismark-600 font-bold underline hover:text-edtech-blue-900">
							reg&iacute;strese
						</a>
					</p>
				</div>

				<LoginForm />

				<div className="flex gap-2 w-full items-center justify-center py-2">
					<hr className="w-full" />
					<span className="w-fit text-nowrap text-center">
						o inicie sesión con
					</span>{" "}
					<hr className="w-full" />
				</div>

				<button
					className="py-3 px-4 w-48 flex gap-2 border border-red-500 rounded-md text-red-500 hover:bg-red-100 justify-center items-center cursor-pointer"
					onClick={handleSingInGoogle}>
					<GoogleIcon className="h-6 w-6" />
					Google
				</button>
			</div>

			<div className="h-full sm:block hidden w-full">
				<Image
					src="/login/image01.webp"
					alt="Imagen de inicio de sesión"
					width={1280}
					height={854}
					className="rounded-md md:rounded-bl-[10rem] rounded-bl-[5rem] rounded-tr-[5rem] md:rounded-tr-[10rem] object-none object-center h-full w-auto"
				/>
			</div>
		</section>
	);
}

export default LoginMain;

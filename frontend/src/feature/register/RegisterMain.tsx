"use client";

import Image from "next/image";
import RegisterForm from "./RegisterForm";
import Link from "next/link";

function RegisterMain() {
	return (
		<section className="flex bg-edtech-blue-100 rounded-md md:h-full w-full p-5 md:p-10 gap-5 lg:gap-10 max-w-[1440px] h-[100hv]">
			<div className="bg-white overflow-y-auto flex flex-col h-full gap-2.5 md:gap-5  rounded-md px-5 py-3 md:p-5 shadow-2xl items-center md:pb-10  w-2/3">
				{/* <Image
					src="/logo.webp"
					alt="Edtech avance con IA"
					width={669}
					height={669}
					className="h-24 lg:h-[7rem] w-24 lg:w-[7rem] object-center"
				/> */}
				<div className="flex flex-col gap-3 w-full">
					<h1 className="text-3xl font-bold">Registrar usuario</h1>
					<p className="text-base">
						¿Ya tienes una cuenta?{" "}
						<Link
							href="/login"
							className="text-bismark-600 font-bold underline hover:text-edtech-blue-900 outline-none">
							Inicie sesión
						</Link>
					</p>
				</div>

				<RegisterForm />
			</div>

			<div className="h-full">
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

export default RegisterMain;

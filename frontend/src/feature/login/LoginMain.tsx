"use client";

import { useFormik } from "formik";
import React from "react";
import LoginForm from "./LoginForm";
import { LoginImage } from "@/assets/unDraw";
import { GoogleIcon } from "@/assets/socialIcon";
import { signIn } from "next-auth/react";

function LoginMain() {
	const handleSingInGoogle = () => {
		signIn("google", { callbackUrl: "/" });
	};

	return (
		<section className="flex bg-bismark-100 rounded-2xl h-[calc(100vh-80px)] max-h-[670px] w-full p-10 gap-10 max-w-[1440px] ">
			<div className="bg-white flex flex-col h-full gap-10 w-1/2 rounded-md p-5 shadow-2xl">
				<div className="flex flex-col gap-3">
					<h1 className="text-3xl font-bold">Inicio de sesión</h1>
					<p className="text-sm">
						¿Aún no tiene una cuenta?{" "}
						<a href="" className="text-bismark-600 font-bold">
							reg&iacute;strese
						</a>
					</p>
				</div>

				<LoginForm />

				<div className="flex gap-2 w-full items-center justify-center">
					<hr className="w-full" />
					<span className="w-fit text-nowrap text-center">
						o inicie sesión con
					</span>{" "}
					<hr className="w-full" />
				</div>

				<div className="flex gap-5 w-full justify-center">
					<button
						className="py-3 px-4 w-48 flex gap-2 border border-red-500 rounded-md text-red-500 hover:bg-red-100 justify-center items-center cursor-pointer"
						onClick={handleSingInGoogle}>
						<GoogleIcon className="h-6 w-6" />
						Google
					</button>
				</div>
			</div>

			<div className="flex w-full h-full justify-items-center justify-center">
				<LoginImage className="w-full h-auto" />
			</div>
		</section>
	);
}

export default LoginMain;

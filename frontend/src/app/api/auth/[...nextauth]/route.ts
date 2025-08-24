import NextAuth, { NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import GoogleProvider from "next-auth/providers/google";

export const authOptions: NextAuthOptions = {
	providers: [
		GoogleProvider({
			clientId: process.env.GOOGLE_CLIENT_ID!,
			clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
		}),
		CredentialsProvider({
			name: "Credentials",
			credentials: {
				email: { label: "Email", type: "email" },
				password: { label: "Password", type: "password" },
			},
			async authorize(credentials) {
				if (!credentials?.email || !credentials?.password) return null;

				const res = await fetch(
					`${process.env.NEXT_PUBLIC_AUTH_URL}/auth/login`,
					{
						method: "POST",
						headers: { "Content-Type": "application/json" },
						body: JSON.stringify({
							email: credentials.email,
							password: credentials.password,
						}),
					}
				);

				if (!res.ok) return null;

				const user = await res.json();
				return user;
			},
		}),
	],
	callbacks: {
		async signIn({ account }) {
			if (account?.provider === "google") {
				const { id_token } = account;

				try {
					const res = await fetch(
						`${process.env.NEXT_PUBLIC_AUTH_URL}/auth/social-login`,
						{
							method: "POST",
							headers: { "Content-Type": "application/json" },
							body: JSON.stringify({
								id_token,
							}),
						}
					);

					if (!res.ok) {
						console.error("Backend error (social-login)", res);
						return false;
					}
				} catch (err) {
					console.error("Error comunicando con backend:", err);
					return false;
				}
			}
			return true;
		},
		async session({ session, token, user }) {
			// Puedes personalizar la sesión aquí si quieres
			console.log("token", token, user);
			return session;
		},
	},
	pages: {
		signIn: "/login",
	},
	secret: process.env.NEXT_AUTH_SECRET,
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };

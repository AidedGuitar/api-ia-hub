import NextAuth, { NextAuthOptions } from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";

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

				const res = await fetch("http://localhost:8000/auth/login", {
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({
						email: credentials.email,
						password: credentials.password,
					}),
				});

				if (!res.ok) return null;

				const user = await res.json();
				return user;
			},
		}),
	],
	callbacks: {
		async signIn({ user, account }) {
			if (account?.provider === "google") {
				try {
					const res = await fetch(
						"http://localhost:8000/auth/social-login",
						{
							method: "POST",
							headers: { "Content-Type": "application/json" },
							body: JSON.stringify({
								email: user.email,
								name: user.name,
							}),
						}
					);

					if (!res.ok) {
						console.error("Backend error (social-login)");
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
	secret: process.env.NEXTAUTH_SECRET,
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };

"use server";
import { sql } from "@vercel/postgres";

import TypeEffect from "./typeEffect";

const getMessage = async () => {
	console.log("get message");
	try {
		const result =
			await sql`SELECT message FROM messages ORDER BY id DESC LIMIT 1`;

		return result.rows[0]?.message || "Pas de message disponible";
	} catch (error) {
		console.error(error);
	} finally {
	}
};

const Message = async () => {
	const message = await getMessage();
	return (
		<div className="w-96">
			<TypeEffect message={message ? message : "Aucun message trouvé"} />
		</div>
	);
};

export default Message;

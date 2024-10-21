"use client";
import { useState, useEffect } from "react";
import TypeEffect from "./typeEffect";

const DisplayMessage = () => {
	const [currentMessage, setCurrentMessage] = useState("");
	const [currentColor, setCurrentColor] = useState("#111111");
	const [hasError, setHasError] = useState(false);

	// Fonction pour récupérer le message actuel
	const fetchCurrentMessage = async () => {
		try {
			const response = await fetch("/api/py/readMessage", {
				cache: "no-cache", // Ne pas utiliser le cache },
			});

			const { message, color } = await response.json();
			setCurrentMessage(message);
			setCurrentColor(color);
		} catch (error) {
			setHasError(true);
			console.error("Erreur lors du fetch:", error);
		}
	};

	// useEffect pour récupérer les données et simuler la revalidation
	useEffect(() => {
		// Appeler fetch pour initialiser les données
		fetchCurrentMessage();

		// Polling : répéter le fetch toutes les X secondes pour vérifier si le message a changé
		const interval = setInterval(() => {
			fetchCurrentMessage();
		}, 5000); // Mettre à jour toutes les 5 secondes, ou selon ton besoin

		// Cleanup de l'intervalle à la fin
		return () => clearInterval(interval);
	}, []);

	if (hasError) {
		return <p>Erreur lors du chargement du message.</p>;
	}

	return (
		<div
			style={{
				color: currentColor,
			}}
			className="w-96 h-56 text-center"
		>
			<TypeEffect message={currentMessage} />
		</div>
	);
};

export default DisplayMessage;

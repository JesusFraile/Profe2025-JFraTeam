#Importing libraries
from dotenv import load_dotenv
import os
from utils import utils
from agents import responder, evaluator

#Constants

load_dotenv() # Load .env variables
API_KEY = os.getenv("API_KEY")
SET_PATH='datasets/train_set.json'

#Starting main structure
df=utils.load_dataset(SET_PATH)

model=responder.responderAgent(API_KEY)
model_evaluator=evaluator.evaluatorAgent(API_KEY)

exercise='ACTIVIDADES CULTURALES Y DE OCIO\nTEATRO\n1. Carta de amor. La última obra de Fernando Rabal, se la ha dedicado a su madre y por eso está llena de sentimientos. El texto fue estrenado en enero en el teatro Reina Sofía, y se mueve entre la novela y la poesía. Entrada: 10 €. No hay entradas\n2. Luces de Bohemia. Helena Pimenta, una de las directoras de teatro más importantes de España, dirige el drama “Luces de bohemia”en el teatro Cervantes de Teruel abierto al público desde 1479. La directora ha estado trabajando 2 años en esta obra.  Entrada: de 6 a 9 €.\n3. Pan con pan. Es un texto dirigido por Miguel Muñoz. La obra está llena de personajes en la que se recuerda a los más pobres de la sociedad. En esta obra hay humor, poesía y crítica social. Ha sido premio Max de teatro 2002. Entrada con descuento para estudiantes.\n4. Defensa de Sancho Panza. El autor y director Fernando Fernán Gómez estrenó ayer esta obra en el teatro Infanta Isabel, en Madrid. En ella el protagonista tiene que defend-erse de algunos delitos. “La idea ni es original ni es mía”, ha dicho el famoso director. Entrada: 15 €.\nMÚSICA\n1. The Fairy Queen. Lindsay Kemp pensó en la película “El sueño de una noche de vera-no” para hacer esta obra. Es una mezcla de música, teatro y baile. Esta obra podremos verla las próximas Navidades.\n2. La flauta mágica de Mozart, interpretada por la compañía El Teatro Negro de Praga. Durante el mes de octubre podemos  ver y escuchar La flauta mágica en el teatro Maravillas de Jaén. La obra añade a la música el encanto de un espectáculo sin palabras.\n3. Música religiosa en las catedrales. En las catedrales de Madrid, Plasencia y Salamanca se podrá escuchar este concierto el próximo mes de mayo, interpretado por La Orquesta de la Comunidad de Madrid dedicado a Juan Sebastián Bach. Está organizado por la Fundación Caja Madrid.\n4. Broadway. Es el musical más famoso de todos los tiempos. Durante estos días se puede ver en El Teatro de la Ópera Nacional de Krasnodarsk en Rusia. Otro atractivo de esta obra será ver el espectáculo de luces y colores con los últimos avances tecnológicos.\nVIAJES\n1. Hervás (Cáceres). Duración:\ndel 4 al 7 de abril. Precio: a partir de 250 €. Organiza: Halcón Viajes. Programa de cuatro días con natación y paseos a caballo. El precio también incluye el alojamiento en un hotel de tres estrellas con pensión completa. Viaje ahora y pague en los próximos meses.\n2. Doñana (Huelva). Duración: del 4 al 7 de abril. Precio: 200 €. Organiza: Gente Viajera. Cuatro días en contacto directo con la naturaleza. Se realizarán excursiones por la montaña. Alojamiento en hotel de tres estrellas, con pensión completa (desayuno, comida y cena).\n3. París (Francia). Duración: del 4 al 7 de abril. Precio: 342 €, con vuelo desde Madrid y 350 € desde Barcelona. Preguntar precios desde otras ciudades. Organiza: Viajes Barcelona. Uno de los mejores precios de la temporada, ya que incluye el transporte desde el aeropuerto hasta el hotel, el alojamiento con desayuno, guía y seguro de viaje.\n4. Milán, Florencia y Génova (Italia). Duración: del 2 al 7 de abril. Precio: 1.168 €, con vuelo desde Barcelona y 1.198 € desde Madrid. Organiza: Turismúsica. Además de los vuelos, alojamiento con desayuno en hoteles de cuatro estrellas y seguro de viaje, este programa ofrece visitas culturales guiadas por Milán, Florencia, Pisa y Génova. También incluye las entradas a tres conciertos.\n5. Menorca (Islas Baleares). Duración: del 1 al 8 de abril. Precio: 301 €, con vuelo desde Madrid. Consultar precios desde otras ciudades. Organiza: Águila Viajes. Perfecto para familias que quieran unas vacaciones de sol y playa. Transporte, alojamiento en régimen de media pensión (desayuno, comida o cena) y seguro incluidos.'
question='¿En qué viaje están incluidas todas las comidas?'
options=['Doñana.', 'París.', 'Menorca.']

a,b=model.do_inference(exercise, question, options)
print('='*8)
print(a)
print('='*8)
print(b)
n=utils.convert_letter_to_number(a)

c, d=model_evaluator.do_inference(exercise, question, options[1])
print('='*8)
print(c)
print('='*8)
print(d)


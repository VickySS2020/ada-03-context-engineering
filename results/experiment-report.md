# Context Engineering Experiment
En este experimento, observaremos cómo cambia el comportamiento del agente después de ejecutar la misma tarea sobre el código de un programa en tres diferentes condiciones de contexto: mínimo, contexto del repositorio y contexto diseñado. 

## Hypothesis
Se tiene pensado que entre más especificaciones se dé al agente este hará un mejor trabajo, es decir, cumplirá con todos los requisitos, hará pocos cambios innecesarios y en el menor tiempo posible. Por lo que, se esperá que el experimento A, haga la mayor cantidad de cambios innecesarios y que cumplan con unos cuantos de los requisitos. El experimento B hará la menor cantidad de cambios innecesarios y cumpla con mayoría de los requisitos. Y el experimento C, cumpla con todos los requisitos y no haga cambios innecesarios.

## Experimental Setup
Para este experimento creamos un repositorio con la rama “main”, la cual contendrá el código base proporcionado por el documento “ADA-03 — Context Engineering Experiment”.  Después, creamos 3 ramas (a,b y c) que contendrán el mismo código base, a excepción de la c que incluirá los archivos SPEC.md y AGENTS.md; sobre estas ramas trabajará el agente para la ejecución de la tarea.

## A — Minimal Context
Prompt: 
Implement the customer email update functionality.
Inspect the repository first. Implement the necessary changes and run the tests.

Results: El agente hizó todos los cambios necesarios para resolver los errores presentes en el código fuente (validar el correo sintácticamente y convertirlo a mínuscula) y cumplió con todos los requisitos, aunque agregó casos de prueba a test_customer.py y test_repository.py que podrían verse como innecesarios. Igualmente, introdujo un problema posterior a la implementación de los cambios, pues la función update_customer_email(), no revisa que “updated_by” sea un string válido.

Human intervention: A parte de dar permisos al agente para ejecutar comandos y modificar archivos, tuve que arreglar el problema de validación de "updates_by".

Score: 89

Observations: El agente agregó 4 pruebas de más incluso si no eran necesarias, y modificó más archivos de lo necesarios(test_customer.py y test_repository.py).

## B — Repository Context
Prompt: 
Implement the customer email update functionality.
Before making changes:
1. Inspect the repository.
2. Read README.md.
3. Inspect all relevant source files.
4. Inspect the tests.
5. Infer expected behavior from the code and tests.
6. Run tests before changing code.
7. Make the smallest necessary implementation.
8. Run tests again.
9. Explain which repository information influenced the implementation.

Results: El agente no modificó las pruebas y sólo hizó cambios a los documentos customer.py y repository.py. Se pasaron todas las pruebas, sin embargo, la validación de gmail es incorrecta debido a que únicamente revisa si un string tiene el símbolo '@' en vez de revisar su sintaxis para verificar que tenga una estructura de correo válida.

Human intervention: A parte de dar permisos al agente para ejecutar comandos y modificar archivos, tuve que arreglar el problema en la validación de correo.

Score: 87.1
Observations: Parece que el agente se tomo menor tiempo pensando en cómo resolver el problema e hizó menos cambios innecesarios, sin embargo, debido a que se le pidió hacer un implementación pequeña, no se complicó demasiado al implementar la validación del correo.

## C — Engineered Context
Prompt: 
Implement the customer email update functionality.
Follow SPEC.md and AGENTS.md.
Inspect the repository first, run tests before and after changes, and explain your verification.

Results: Se hicieron cambios únicamente a los archivos customer.py y repository.py, se pasaron todas las pruebas(sin casos de prueba adicionales a los 4 principales) y el código cumple con todos los requisitos. No hubo cambios innecesario, aunque tuvo el mismo problema del experimento A (falta de validación de updated_by).

Human intervention: A parte de dar permisos al agente para ejecutar comandos y modificar archivos, tuve que arreglar el problema en la validación de updated_by.

Score: 90
Observations: El agente tómo mayor tiempo que el experimento B en encontrar un solución pero menor tiempo que el experimento A. Con las especificaciones en los documentos SPEC.md y AGENTS.md pudo discernir el contexto de todo el programa e implementar correctamente cambios (no modificar tests y validar el correo sintácticamente).

## Comparative Results
El experimento C produjo el mejor resultado. Obtuvo el score más alto, con 90/100, frente a 89/100 en A y 87.1/100 en B. Además, C cumplió todos los requisitos funcionales, pasó los cuatro tests originales y modificó únicamente customer.py y repository.py, sin agregar casos de prueba innecesarios.

La principal diferencia fue la calidad del contexto proporcionado. En C, el agente recibió SPEC.md que especificaba, entre otras cosas, que el email debía ser lowercase y tener una sintaxis válida, mientras que AGENTS.md indicaba realizar el cambio mínimo y no modificar los tests salvo que fuera necesario.

Ambos experimentos A y C cumplieron con los requisitos, a excepción de B que no cumplió la validación de correo por sintaxis, esto posiblemente debido a que el prompt le especificó a hacer cambios pequeños por lo que el agente probablemente simplicó la validación del correo para cumplir con esta demanda. Ambos B y C no hicieron modificaciones a archivos de manera innecesaria, a excepción de A que modificó los archivos test_repository.py y test_customer.py para agregar casos de prueba no requeridos.

## Error Analysis
En el experimento A apareció un error que no apareció en C: el agente agregó 4 casos de prueba adicionales y modificó test_customer.py y test_repository.py, aunque los tests no necesitaban ser modificados. En cambio, C se limitó a modificar customer.py y repository.py y mantuvo los cuatro tests originales; lo cual coincide directamente con la instrucción de AGENTS.md de no modificar tests salvo que se solicite explícitamente.

En el experimento B, el agente no implementó validación de correo sintáctica a diferencia de los experimentos A y C debido a la falta de especificación (no se anotó el tipo de validación) y el impulso a hacer modificaciones pequeñas en el prompt.

Sin embargo, A y C compartieron un mismo problema: ambos dejaron sin validar correctamente updated_by. Por ello, el contexto diseñado mejoró considerablemente el comportamiento del agente, pero no eliminó todos los posibles errores.

Todos los experimentos crearon pytest.ini, que fue considerado como un cambio innecesario.

## Context Quality Analysis
La información más útil del repositorio fue el código fuente, README y tests. El README le explica al agente la estructura del proyecto y señala que customer.py contiene las operaciones del dominio, mientras que repository.py contiene el repositorio de clientes; y Los tests, por su parte, expresan comportamientos con los que debe cumplir el programa para ser considerado exitoso.

Los documentos como SPEC.md y AGENTS.md también sirvieron para expresar explícitamente los requisitos y comportamientos específicos deseados para el programa y el agente. Con SPEC.md aportando la definición explícita de los requisitos, indicando que el email debía actualizarse, estableciendo condiciones concretas como la existencia del cliente, validación sintáctica del email, conservación del ID y created_by, y la actualización de updated_by. Esto ayudó a evitar la solución incompleta observada en el experimento B, donde el agente solamente comprobó la presencia de @. Y con AGENTS.md definiendo las reglas de comportamiento del agente indicando que debía inspeccionar antes de editar, realizar el cambio mínimo, no modificar tests y ejecutar las pruebas antes y después. Lo que explica por qué C evitó los cambios adicionales observados en el experimento A.

El experimento también demuestra que dar más contexto no necesariamente significa dar mejor contexto; pues B recibió instrucciones para inspeccionar ampliamente el repositorio y aun así obtuvo un resultado inferior a C debido a la falta de especificaciones como las contenidas en SPEC.md y AGENTS.md.

La información redundante fue principalmente la relacionada con ejecutar los test directamente mediante pytest. La creación del archivo 'pytest.ini' fue considerada innecesaria en A, B y C, porque las pruebas podían ejecutarse mediante python -m pytest.

## Conclusions
Este experimento se muestra que utilizar un agente de código no elimina la responsabilidad del desarrollador; la transforma. El desarrollador sigue siendo responsable de definir claramente el objetivo, proporcionar el contexto adecuado, establecer restricciones y verificar que el resultado realmente cumple con los requisitos.

El experimento C obtuvo el mejor resultado porque el agente no recibió solamente más información, sino información estructurada mediante SPEC.md y AGENTS.md. Con SPEC.md definiendo lo que debía cumplir la implementación creada por el agente, y AGENTS.md estableciendo cómo debía trabajar el agente y qué cambios debía evitar.

Lo anterior demuestra la razón por la que un desarrollador que utiliza agentes necesita aprender de Context Engineering y no solamente aprender a escribir mejores prompts. Un prompt puede describir una tarea, pero el Context Engineering permite diseñar un entorno de información y reglas que reduzca ambigüedades, oriente las decisiones del agente y limite los cambios innecesarios.

Además, un agente puede producir una solución que pase todos los tests y aun así contenga problemas, como ocurrió con la validación de ‘updated_by’; por eso, el desarrollador debe revisar, probar y cuestionar las decisiones del agente. Un agente puede acelerar la implementación, pero la responsabilidad sobre la calidad y correctitud del software todavía recae en el ser humano.

## What I Would Change
Yo haría más explícitos los requisitos que quedaron ambiguos, especialmente la validación de updated_by. Actualmente SPEC.md dice que updated_by debe “contener al actor realizando la actualización”, pero no define qué constituye un valor válido o si siguiera hay que verificar que sea un string.

En AGENTS.md, agregaría más reglas como: verificar cada requisito en SPEC.md individualmente, correr las pruebas usando el comando pytest o python -m pytest, reportar cualquier requisito que no pudo ser verificado, entre otros.

En README agregaría a Run test el comando python -m pytest.
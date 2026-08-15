# Política de seguridad

## Versiones cubiertas

La rama `main` y la última versión estable de la serie 1.x reciben correcciones de seguridad y mantenimiento cuando sean necesarias. Las releases científicas publicadas permanecen inmutables como objetos de registro; una vulnerabilidad detectada después se corrige en una nueva versión, no reescribiendo retrospectivamente el snapshot citado.

## Qué se considera un problema de seguridad

Reporte de manera privada situaciones como:

- exposición de credenciales, tokens o secretos;
- vulnerabilidades que permitan ejecución no autorizada, modificación del servicio o acceso indebido;
- dependencias comprometidas con impacto real en el pipeline o despliegue;
- filtración de datos personales no destinados a publicación;
- mecanismos que permitan alterar artefactos científicos sin dejar trazabilidad.

Los errores de transcripción, desacuerdos filológicos, problemas de metadatos, enlaces rotos y bugs ordinarios del pipeline **no son vulnerabilidades de seguridad**; deben reportarse mediante issues públicos cuando no involucren información sensible.

## Cómo reportar

No publique secretos ni pruebas de explotación sensibles en un issue abierto. Utilice las funciones privadas de reporte de seguridad de GitHub cuando estén disponibles para el repositorio. Si esa vía no aparece habilitada, contacte al mantenedor a través de un canal académico verificable indicado en su perfil público, compartiendo únicamente la información necesaria para reproducir el problema.

Incluya, cuando sea posible:

- componente o archivo afectado;
- versión/commit;
- descripción del impacto;
- pasos mínimos de reproducción;
- evidencia técnica;
- propuesta de mitigación, si la tiene.

## Integridad científica

RHD considera la **integridad de procedencia** parte de su superficie de seguridad. Los cambios que puedan modificar silenciosamente datos canónicos, hashes, manifiestos o resultados derivados deben tratarse con especial cuidado incluso si no constituyen una vulnerabilidad informática convencional.

## Divulgación

Una vez corregido un problema de seguridad relevante, el proyecto procurará documentar el alcance y la versión corregida sin revelar información que facilite abuso innecesario. Cuando una corrección cambie resultados científicos o artefactos de investigación, también deberá seguir las reglas de versionado y `CHANGELOG.md`.

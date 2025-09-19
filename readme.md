# Análise dos Algoritmos

### ❓ O Hill Climbing travou em soluções locais?
Ao analisar as diversas execuções do algoritmos é possível avaliar que o algoritmo HC não travou em soluções locais, pois tivemos uma baixa variação, com valores entre **R$310 e R$340**, então é válido dizer que é uma solução comportada.

---

### ❓ O Simulated Annealing conseguiu escapar de ótimos locais?
Mesmo que o fitness ficasse pior em alguns momentos da execução, principalmente em altas temperaturas, o **SA conseguiu encontrar soluções melhores ou iguais ao HC**.

---

### ❓ O Algoritmo Genético trouxe diversidade e soluções mais próximas do ótimo?
O **AG explorou várias soluções** por meio da população diversificada de indivíduos (50). Ele gradualmente refina a sua solução, nos trazendo ao final da execução **soluções boas e satisfatórias mesmo com a penalidade**, mostrando que ainda penalizadas, temos boas soluções.

---

### ❓ Qual método foi mais rápido? E qual foi mais eficaz?
O **HC foi o método mais veloz**, mas com base nos valores por limite de peso o **AG se saiu melhor**.

---

### ❓ Os três algoritmos são estocásticos. Explique o que significa serem estocásticos e o que diferencia de um que não seja
Os **algoritmos estocásticos** são os que utilizam de **aleatoriedade** na solução, resultando em diferentes comportamentos em cada execução.  
Já os **algoritmos determinísticos** sempre irão reproduzir uma mesma saída dado uma mesma entrada.

/** 
 * @file frontend/site/script/locale.js
 * 
 * @author AndreiCristeli
 * 
 * @version 0.1
 */

const resources = {
  pt: {
    translation: {
      title: "Saiki",
      question: "Qual é o algoritmo do dia?",
      inputPlaceholder: "Escreva aqui",
      attempts: "Tentativas: ",
      howToPlay: "Como jogar",
      description: "Você deve adivinhar o algoritmo do dia se baseando nas pistas.",
      categoryInfoTitle: "Categoria",
      categoryInfoText: "O tipo ou propósito geral do algoritmo. Ex: ordenação, busca, grafos, otimização, geometria computacional.",
      yearInfoTitle: "Ano",
      yearInfoText: "Ano de criação ou publicação do algoritmo. Refere-se ao momento em que o algoritmo foi proposto ou documentado pela primeira vez.",
      timeInfoTitle: "Complexidade Temporal Média",
      timeInfoText: "Tempo esperado que o algoritmo leva para executar em casos comuns. Representada em notação Big-O: O(n), O(n log n), etc.",
      spaceInfoTitle: "Complexidade Espacial Auxiliar",
      spaceInfoText: "Memória extra necessária além da entrada original. Também expressa em Big-O, como O(1), O(n). Não conta a memória ocupada pelos dados de entrada.",
      structureInfoTitle: "Estrutura de Dados",
      structureInfoText: "As estruturas usadas para processar a informação. Ex: listas, filas, pilhas, árvores, heaps, tabelas hash.",
      solutionInfoTitle: "Solução",
      solutionInfoText: "Tipo de abordagem adotada pelo algoritmo. Exata: resolve o problema com resposta correta garantida. Aproximada: gera uma solução próxima da ideal. Heurística: usa regras práticas para encontrar boas soluções.",
      generalityInfoTitle: "Generalidade",
      generalityInfoText: "O algoritmo soluciona qualquer tipo de problema dentro da sua categoria ou exige certas condições? Ex: BubbleSort ordena qualquer vetor. RadixSort exige inteiros."
    }
  },
  en: {
    translation: {
      title: "saiki",
      question: "What is today's algorithm?",
      inputPlaceholder: "Type here",
      attempts: "Attempts: ",
      howToPlay: "How to play",
      description: "You must guess the algorithm of the day based on the clues.",
      categoryInfoTitle: "Category",
      categoryInfoText: "The general type or purpose of the algorithm. E.g., sorting, search, graphs, optimization, computational geometry.",
      yearInfoTitle: "Year",
      yearInfoText: "Year of creation or publication. Refers to when the algorithm was first proposed or documented.",
      timeInfoTitle: "Average Time Complexity",
      timeInfoText: "Expected time the algorithm takes to run on typical input. Expressed in Big-O notation: O(n), O(n log n), etc.",
      spaceInfoTitle: "Auxiliary Space Complexity",
      spaceInfoText: "Extra memory needed beyond the input. Also in Big-O, like O(1), O(n). Does not count the memory used by input.",
      structureInfoTitle: "Data Structure",
      structureInfoText: "Structures used to process data. E.g., lists, queues, stacks, trees, heaps, hash tables.",
      solutionInfoTitle: "Solution",
      solutionInfoText: "Approach type. Exact: gives guaranteed correct answer. Approximate: gives near-optimal solution. Heuristic: uses practical rules for good (but not guaranteed) answers.",
      generalityInfoTitle: "Generality",
      generalityInfoText: "Does it solve any problem in its category or does it need specific conditions? E.g., BubbleSort works on any list; RadixSort needs integers."
    }
  }
};

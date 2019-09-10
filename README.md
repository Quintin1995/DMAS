# DMAS
Design of Multi Agent Systems Repository.
Date: Friday 06-09-2019

\begin{itemize}
    \item Agent : Int
    \item Agents : [Dict]
    \begin{itemize}
        \item Agents['Secrets'] : [Bool]
        \begin{itemize}
            \item Knowledge of agent X : Secrets[X] ([Bool], e.g. : [TRUE, FALSE, FALSE])
            \item Does agent X know agent Y's secret? : Secrets[X][Y] (Bool, e.g. TRUE) 
        \end{itemize}
    \end{itemize}
    
    \item Calls : [Tuple (Calling_Agent, Receiving_Agent)]
    \begin{itemize}
        \item Has agent X called agent Y? : (Calling_Agent, Receiving_Agent) in Calls
        \item Keuze voor list of tuples omdat dan de volgorde van de calls ook wordt bijgehouden.
    \end{itemize}
    \item Protocols : Function 
    \begin{itemize}
        \item E.g. make_call_lns (Agents, Calls)
    \end{itemize}
\end{itemize}

* Protocols:
  - ANY
  - LNS
  - CO
  - TOK
  - SPIDER
 * Generate Graphs
 * GUI?
 * Add and Remove Agents
 * Lying Agents? Accidentally given different information.
 * Stress Test
 * Statistics Class
  -This class runs X amount of experiments and gathers results and makes nice plots.
  

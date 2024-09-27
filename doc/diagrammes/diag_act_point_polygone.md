@startuml
start

  :Vérifier si le point est dans le rectangle;
  if (Dans le rectangle?) then (oui)
    :Vérifier si le point est dans le polygone principal;
    if (Dans le polygone principal?) then (oui)
      :Vérifier les inclaves;
      if (Dans un inclave?) then (oui)
        :Retourner False (le point est en dehors);
      else (non)
        :Retourner True (le point est dedans);
      endif
    else (non)
      :Vérifier les exclaves;
      if (Dans un exclave?) then (oui)
        :Vérifier récursivement les inclaves dans cet exclave;
      else (non)
        :Retourner False (le point est en dehors);
      endif
    endif
  else (non)
    :Retourner False (le point est en dehors);
  endif
end
@enduml
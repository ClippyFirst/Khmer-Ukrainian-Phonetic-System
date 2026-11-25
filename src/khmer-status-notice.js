function getStatusNotice(data) {
  if (!data) return "";
  if (data.selected_external_candidate) {
    return "Показано зовнішній IPA-кандидат від " + data.selected_external_candidate.provider
      + ". Це неперевірений широкофонетичний результат: profile_match=UNVERIFIED, незалежної ад'юдикації немає. ??? наприкінці IPA та українського зіставлення позначає весь результат як PROVISIONAL; інші виходи провайдерів збережено в деталях.";
  }
  if (data.ukrainian_output_kind === "ORTHOGRAPHIC_ROMANIZATION_FALLBACK") {
    return "Український рядок містить попередню орфографічну підказку з романізації, а не підтверджену вимову. ??? позначає невстановлену фонетичну частину; IPA залишається окремо невстановленою.";
  }
  if (data.ukrainian_output_kind === "ORTHOGRAPHIC_FALLBACK") {
    return "Український рядок показує окрему орфографічну підказку за написанням, а не підтверджену вимову. Вона не є результатом IPA-адаптації; невстановлену фонетичну частину позначено ???.";
  }
  if (data.ukrainian_output_kind === "IPA_DERIVED_PARTIAL") {
    return "Показано лише низькодостовірні IPA-підказки відомих початкових приголосних. Знак ??? позначає невстановлену частину; голосні, фіналі й тон не вгадуються.";
  }
  if (data.ukrainian_output_kind === "IPA_DERIVED_PROVISIONAL") {
    return "Показано локальний фонемний словниковий кандидат, перетворений на IPA й українську форму. Він має статус PROVISIONAL: відповідність словникового профілю цільовому профілю не підтверджена незалежною ад'юдикацією.";
  }
  if (data.ukrainian_output_kind === "NEURAL_DISTILLED_IPA_PROVISIONAL") {
    return "Показано локальний детермінований кандидат, скомпільований з офлайнової нейромережевої дистиляції. Він має статус PROVISIONAL і не є незалежно підтвердженою вимовою.";
  }
  if (data.ukrainian_output_kind === "EXTERNAL_IPA_PROVISIONAL" || data.status === "PROVISIONAL") {
    return "Показано попередній IPA-кандидат зі статусом PROVISIONAL; його джерело та відповідність цільовому профілю слід перевірити.";
  }
  if (data.status === "PROPOSED") {
    return "Результат має статус PROPOSED: IPA та українське читання є дослідницькими пропозиціями для цих записів, а не підтвердженою універсальною моделлю. Перевіряйте джерела й лексичний контекст перед використанням.";
  }
  if (data.status === "EVIDENCE_LIMITED" || data.status === "NOT_ESTABLISHED") {
    return data.note;
  }
  if (data.status === "INVALID_OR_UNSUPPORTED") {
    return "Ввід не підтримується повністю. Перегляньте статус кожної одиниці та не використовуйте маркери непідтвердженого результату як вимову.";
  }
  return "";
}

export { getStatusNotice };

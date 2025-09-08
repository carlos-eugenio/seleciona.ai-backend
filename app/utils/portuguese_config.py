"""
Configurações específicas para processamento de texto em português brasileiro
"""

# Palavras-chave produtivas em português brasileiro
PRODUCTIVE_KEYWORDS = [
    # Urgência e prazo
    'urgente', 'urgência', 'asap', 'prazo', 'deadline', 'data limite',
    'hoje', 'amanhã', 'imediatamente', 'já', 'agora', 'rapidamente',
    'emergência', 'emergencia', 'crítico', 'critico', 'prioridade',
    
    # Reuniões e compromissos
    'reunião', 'reuniao', 'meeting', 'encontro', 'agendamento', 'agenda',
    'compromisso', 'apresentação', 'apresentacao', 'conferência', 'conferencia',
    'call', 'videoconferência', 'videoconferencia', 'webinar',
    
    # Projetos e tarefas
    'projeto', 'project', 'tarefa', 'task', 'atividade', 'ação', 'acao',
    'trabalho', 'job', 'entrega', 'delivery', 'execução', 'execucao',
    'desenvolvimento', 'implementação', 'implementacao', 'criação', 'criacao',
    
    # Necessidades e solicitações
    'necessário', 'necessario', 'preciso', 'precisa', 'required', 'needed',
    'solicitação', 'solicitacao', 'request', 'pedido', 'demanda', 'requisito',
    'obrigatório', 'obrigatorio', 'essencial', 'fundamental',
    
    # Dúvidas e suporte
    'dúvida', 'duvida', 'question', 'pergunta', 'ajuda', 'help', 'suporte',
    'support', 'assistência', 'assistencia', 'orientação', 'orientacao',
    'consulta', 'esclarecimento', 'explicação', 'explicacao',
    
    # Problemas e correções
    'problema', 'issue', 'erro', 'bug', 'falha', 'defeito', 'inconsistência',
    'inconsistencia', 'corrigir', 'fix', 'resolver', 'solucionar', 'reparar',
    'correção', 'correcao', 'ajuste', 'melhoria', 'otimização', 'otimizacao',
    
    # Atualizações e status
    'atualização', 'atualizacao', 'update', 'status', 'situação', 'situacao',
    'progresso', 'progress', 'andamento', 'evolução', 'evolucao',
    'desenvolvimento', 'crescimento', 'expansão', 'expansao',
    
    # Revisão e aprovação
    'revisar', 'review', 'aprovar', 'approve', 'confirmar', 'confirm',
    'validar', 'verificar', 'checar', 'analisar', 'avaliar', 'examinar',
    'auditoria', 'inspeção', 'inspecao', 'fiscalização', 'fiscalizacao',
    
    # Negócios e trabalho
    'negócio', 'negocio', 'business', 'cliente', 'customer', 'venda', 'sale',
    'contrato', 'contract', 'proposta', 'proposal', 'orçamento', 'orcamento',
    'budget', 'custo', 'cost', 'preço', 'preco', 'price', 'valor',
    'receita', 'lucro', 'profit', 'investimento', 'investment',
    
    # Tecnologia e sistemas
    'sistema', 'system', 'software', 'aplicação', 'aplicacao', 'app',
    'plataforma', 'platform', 'integração', 'integracao', 'api',
    'banco de dados', 'database', 'servidor', 'server', 'hosting',
    
    # Recursos humanos
    'funcionário', 'funcionario', 'employee', 'colaborador', 'equipe',
    'team', 'gestão', 'gestao', 'management', 'liderança', 'lideranca',
    'treinamento', 'training', 'capacitação', 'capacitacao'
]

# Palavras-chave improdutivas em português brasileiro
UNPRODUCTIVE_KEYWORDS = [
    # Agradecimentos e cumprimentos
    'obrigado', 'obrigada', 'thank', 'thanks', 'valeu', 'valeu',
    'parabéns', 'parabens', 'congratulations', 'congrats', 'felicitações',
    'felicitacoes', 'feliz', 'happy', 'alegre', 'contento', 'satisfeito',
    'gratidão', 'gratidao', 'grateful', 'agradecido', 'agradecida',
    
    # Datas especiais
    'aniversário', 'aniversario', 'birthday', 'natal', 'christmas',
    'páscoa', 'pascoa', 'easter', 'ano novo', 'new year', 'feriado',
    'holiday', 'celebration', 'celebração', 'celebracao', 'festa', 'party',
    'comemoração', 'comemoracao', 'festa de aniversário', 'festa de aniversario',
    
    # Convites e eventos sociais
    'convite', 'invitation', 'convida', 'convidar', 'evento', 'event',
    'encontro social', 'social meeting', 'happy hour', 'churrasco',
    'barbecue', 'churrascão', 'churrascao', 'confraternização', 'confraternizacao',
    'festa de formatura', 'formatura', 'graduation', 'casamento', 'wedding',
    'batizado', 'baptism', 'comemoração', 'comemoracao',
    
    # Spam e publicidade
    'spam', 'lixo', 'trash', 'publicidade', 'advertisement', 'propaganda',
    'promoção', 'promocao', 'promotion', 'oferta', 'offer', 'desconto',
    'discount', 'venda', 'sale', 'liquidação', 'liquidacao', 'clearance',
    'marketing', 'ad', 'anúncio', 'anuncio', 'advertisement', 'comercial',
    'promocional', 'promotional', 'cupom', 'coupon', 'desconto', 'discount',
    
    # Newsletters e notícias
    'newsletter', 'boletim', 'notícias', 'noticias', 'news', 'atualização',
    'atualizacao', 'update', 'informações', 'informacoes', 'information',
    'divulgação', 'divulgacao', 'disclosure', 'comunicado', 'announcement',
    'press release', 'comunicado de imprensa', 'nota oficial',
    
    # Conteúdo não profissional
    'piada', 'joke', 'engraçado', 'engracado', 'funny', 'humor', 'comédia',
    'comedia', 'meme', 'vídeo engraçado', 'video engraçado', 'funny video',
    'gif', 'gif engraçado', 'funny gif', 'meme engraçado', 'engracado',
    'hilário', 'hilario', 'hilarious', 'cômico', 'comico', 'comic',
    
    # Mensagens pessoais
    'pessoal', 'personal', 'particular', 'private', 'íntimo', 'intimo',
    'família', 'family', 'amigos', 'friends', 'amigo', 'friend',
    'vida pessoal', 'personal life', 'privado', 'private', 'confidencial',
    'confidential', 'pessoal', 'personal', 'íntimo', 'intimo',
    
    # Conteúdo irrelevante
    'irrelevante', 'irrelevant', 'desnecessário', 'desnecessario',
    'unnecessary', 'inútil', 'inutil', 'useless', 'sem importância',
    'sem importancia', 'unimportant', 'fútil', 'frivolous', 'bobagem',
    'nonsense', 'sem sentido', 'meaningless', 'vazio', 'empty',
    
    # Conteúdo ofensivo ou inadequado
    'ofensivo', 'offensive', 'inadequado', 'inappropriate', 'inapropriado',
    'inconveniente', 'inconvenient', 'desrespeitoso', 'disrespectful',
    'grosseiro', 'rude', 'mal educado', 'mal-educado', 'rude',
    
    # Conteúdo político ou religioso
    'político', 'politico', 'political', 'eleição', 'eleicao', 'election',
    'candidato', 'candidate', 'partido', 'party', 'religioso', 'religious',
    'igreja', 'church', 'templo', 'temple', 'fé', 'faith', 'crença', 'belief'
]

# Respostas automáticas em português brasileiro
PRODUCTIVE_RESPONSES = [
    "Obrigado pelo seu email sobre '{subject}'. Vou analisar e retornar em breve.",
    "Recebi sua mensagem sobre '{subject}'. Vou verificar e fornecer uma resposta detalhada.",
    "Obrigado por entrar em contato sobre '{subject}'. Vou tratar desta questão e responder adequadamente.",
    "Confirmo o recebimento do seu email sobre '{subject}'. Vou processar esta solicitação e retornar em breve.",
    "Obrigado pelo contato. Recebi sua mensagem sobre '{subject}' e vou analisar cuidadosamente.",
    "Confirmo o recebimento do email sobre '{subject}'. Vou verificar os detalhes e retornar com informações.",
    "Obrigado pela sua mensagem sobre '{subject}'. Vou processar esta solicitação e entrar em contato em breve.",
    "Recebi seu email sobre '{subject}'. Vou analisar a situação e fornecer uma resposta completa.",
    "Obrigado pelo email sobre '{subject}'. Vou investigar e retornar com uma solução.",
    "Confirmo o recebimento da sua solicitação sobre '{subject}'. Vou processar e retornar em breve."
]

UNPRODUCTIVE_RESPONSES = [
    "Obrigado pela sua mensagem. Agradeço por pensar em mim.",
    "Obrigado por entrar em contato. Vou manter isso em mente.",
    "Recebi seu email. Obrigado por compartilhar isso comigo.",
    "Obrigado pela sua mensagem. Agradeço a atualização.",
    "Obrigado pelo contato. Aprecio sua consideração.",
    "Recebi sua mensagem. Obrigado por compartilhar.",
    "Obrigado pelo email. Agradeço o pensamento.",
    "Recebi sua comunicação. Obrigado por manter contato.",
    "Obrigado pela mensagem. Agradeço sua atenção.",
    "Recebi seu contato. Obrigado por compartilhar suas ideias."
]

# Configurações de modelo para português
PORTUGUESE_MODEL_CONFIG = {
    "primary_model": "neuralmind/bert-base-portuguese-cased",
    "fallback_model": "distilbert-base-multilingual-cased",
    "confidence_threshold": 0.7,
    "max_length": 512,
    "batch_size": 16
}

# Configurações de pré-processamento para português
PORTUGUESE_PREPROCESSING_CONFIG = {
    "remove_accents": False,  # Manter acentos para português
    "lowercase": True,
    "remove_punctuation": True,
    "remove_numbers": True,
    "min_word_length": 2,
    "max_word_length": 50
}

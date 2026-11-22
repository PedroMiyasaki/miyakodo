"""Fluxos de entrega de serviços. Geometria preta em papel branco, sem ranking numérico."""

STROKE = 'stroke="#0A0A0A" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" fill="none"'
TEXTO = 'font-family="Inter, sans-serif" font-weight="600" font-size="30" fill="#0A0A0A" text-anchor="middle"'


def caixa(x, y, largura, linhas, reticula=False):
    preenchimento = (
        f'<rect x="{x}" y="{y}" width="{largura}" height="140" fill="url(#ht-dark)" '
        'filter="url(#rough2)" transform="translate(-9,7)"/>' if reticula else ''
    )
    texto = ''.join(
        f'<text x="{x + largura / 2}" y="{y + 62 + i * 38}" {TEXTO}>{linha}</text>'
        for i, linha in enumerate(linhas)
    )
    return (preenchimento + f'<rect x="{x}" y="{y}" width="{largura}" height="140" '
            f'{STROKE} filter="url(#rough)"/>' + texto)


def seta(x1, y1, x2, y2):
    return f'<path d="M{x1} {y1} L{x2} {y2}" {STROKE} marker-end="url(#seta)"/>'


def fluxo(entrada, processo, saida):
    return (
        caixa(82, 35, 740, entrada)
        + seta(452, 185, 452, 245)
        + caixa(82, 260, 740, processo, True)
        + seta(452, 410, 452, 470)
        + caixa(82, 485, 740, saida)
    )


FIGURAS = {
    1: fluxo(['Propostas das seguradoras'], ['IA compara condições', 'e prepara formulários'], ['Corretor revisa', 'e apresenta ao cliente']),
    2: fluxo(['Documentos de vários clientes'], ['IA processa rotinas', 'e sinaliza divergências'], ['Equipe revisa exceções', 'e atende mais clientes']),
    3: fluxo(['Notas clínicas'], ['IA aplica regras', 'de codificação'], ['Códigos para faturamento', 'com revisão das exceções']),
    4: (
        caixa(82, 35, 740, ['Apólice + documentação dos danos'])
        + seta(452, 185, 452, 245)
        + caixa(82, 260, 740, ['IA cruza regras e evidências'], True)
        + seta(300, 410, 240, 470) + seta(600, 410, 664, 470)
        + caixa(22, 485, 410, ['Casos padrão', 'Análise agilizada'])
        + caixa(472, 485, 410, ['Exceções', 'Especialista decide'])
    ),
    5: fluxo(['Dados + regras de cada jurisdição'], ['IA processa e cruza', 'as regras aplicáveis'], ['Especialista foca', 'nas decisões complexas']),
}

"""Gráficos reutilizables; mantienen explícita la unidad de incertidumbre."""
import plotly.graph_objects as go

def intervalos_por_paciente(rows):
 fig=go.Figure()
 for row in rows:
  value=row['metricas']['macro_f1']
  low,high=row['IC95_bootstrap_paciente_2000']['macro_f1']
  fig.add_trace(go.Scatter(x=[value],y=[row['modelo']],mode='markers',name=row['modelo'],error_x=dict(type='data',array=[high-value],arrayminus=[value-low]),marker=dict(size=13)))
 fig.update_layout(template='plotly_white',xaxis_title='Macro-F1 e IC descriptivo por paciente (2.000 remuestras)',showlegend=False,xaxis_range=[0,1],margin=dict(l=130))
 return fig

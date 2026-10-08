import streamlit as st
import urllib.parse

# 1. Configuración de pestaña del navegador
st.set_page_config(
    page_title="Slice to Meet You - Pedidos", 
    page_icon="🍕", 
    layout="centered"
)

# ==============================================================================
# CAMBIA AQUÍ TU NÚMERO DE WHATSAPP
# Incluye el código de país sin espacios ni el signo + (Ejemplo Costa Rica: 50688888888)
# ==============================================================================
NUMERO_WHATSAPP = "50600000000"  

# Encabezado principal
st.title("🍕 Slice to Meet You")
st.write("¡Bienvenido! Selecciona tus pizzas favoritas y envía tu orden directa a nuestro WhatsApp.")

# ==============================================================================
# CAMBIA / EDITA AQUÍ TU MENÚ, INGREDIENTES Y PRECIOS
# ==============================================================================
MENU = {
    "Pizza Margherita": {
        "ingredientes": "Salsa de tomate artesanal, queso mozzarella fresco, albahaca", 
        "precio": 10.0
    },
    "Pizza Pepperoni": {
        "ingredientes": "Salsa de tomate, mozzarella, pepperoni curado", 
        "precio": 12.0
    },
    "Pizza Cuatro Quesos": {
        "ingredientes": "Mozzarella, gorgonzola, parmesano, provolone", 
        "precio": 14.0
    },
    "Especial Slice to Meet You": {
        "ingredientes": "Receta especial de la casa con ingredientes de temporada", 
        "precio": 15.0
    }
}

# Inicializar carrito en la sesión
if "carrito" not in st.session_state:
    st.session_state.carrito = {}

# Mostrar Menú interactivo
st.subheader("📜 Nuestro Menú")
for pizza, datos in MENU.items():
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        st.markdown(f"**{pizza}**")
        st.caption(datos["ingredientes"])
    with col2:
        st.write(f"${datos['precio']:.2f}")
    with col3:
        cant = st.number_input(f"Cant.", min_value=0, max_value=10, value=0, key=pizza)
        if cant > 0:
            st.session_state.carrito[pizza] = {"cantidad": cant, "subtotal": cant * datos["precio"]}
        elif pizza in st.session_state.carrito and cant == 0:
            del st.session_state.carrito[pizza]

st.divider()

# Resumen del pedido
st.subheader("🛒 Tu Pedido")

if not st.session_state.carrito:
    st.info("Aún no has seleccionado ninguna pizza.")
else:
    total = 0
    resumen_texto = "🍕 *NUEVO PEDIDO - SLICE TO MEET YOU*\n\n"
    
    for item, detalle in st.session_state.carrito.items():
        st.write(f"• **{item}** x{detalle['cantidad']} = ${detalle['subtotal']:.2f}")
        total += detalle['subtotal']
        resumen_texto += f"• {item} x{detalle['cantidad']} = ${detalle['subtotal']:.2f}\n"
    
    st.markdown(f"### **Monto Total: ${total:.2f}**")
    
    st.divider()
    st.subheader("📍 Datos de Envío")
    nombre = st.text_input("Nombre y Apellido:")
    direccion = st.text_input("Dirección exacta de entrega:")
    notas = st.text_area("Indicaciones / Notas especiales (ej. masa bien tostada, timbre, etc.):")

    if nombre and direccion:
        # Formato del mensaje para WhatsApp
        mensaje_final = f"{resumen_texto}\n"
        mensaje_final += f"💰 *Total a pagar:* ${total:.2f}\n\n"
        mensaje_final += f"👤 *Cliente:* {nombre}\n"
        mensaje_final += f"📍 *Dirección:* {direccion}\n"
        if notas:
            mensaje_final += f"📝 *Notas:* {notas}\n"
            
        mensaje_encoded = urllib.parse.quote(mensaje_final)
        url_whatsapp = f"https://wa.me/{NUMERO_WHATSAPP}?text={mensaje_encoded}"
        
        st.markdown(
            f'''
            <a href="{url_whatsapp}" target="_blank">
                <button style="background-color:#25D366; color:white; border:none; padding:14px 20px; font-size:16px; font-weight:bold; border-radius:8px; cursor:pointer; width:100%;">
                    📲 Enviar Pedido por WhatsApp
                </button>
            </a>
            ''',
            unsafe_allow_html=True
        )
    else:
        st.warning("Escribe tu nombre y dirección para activar el botón de envío por WhatsApp.")

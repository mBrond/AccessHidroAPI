import traceback
import logging
from datetime import datetime
import os
from tkinter import messagebox
from typing import Optional, Callable, Any

class ErrorHandler:
    """
    Classe centralizada para tratamento de erros no projeto AccessHidroAPI
    """
    
    def __init__(self, log_path: str = 'logs'):
        self.log_path = log_path
        self._setup_logging()
    
    def _setup_logging(self):
        """Configura o sistema de logging"""
        os.makedirs(self.log_path, exist_ok=True)
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(self.log_path, 'app.log'), encoding='utf-8'),
                logging.StreamHandler()  # Para console também
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def handle_error(self, 
                    error: Exception, 
                    context: str = "Operação", 
                    show_message: bool = True,
                    log_level: str = "ERROR",
                    custom_message: Optional[str] = None) -> None:
        """
        Trata erros de forma centralizada
        
        Args:
            error: Exceção capturada
            context: Contexto onde o erro ocorreu
            show_message: Se deve mostrar messagebox para o usuário
            log_level: Nível do log (ERROR, WARNING, INFO)
            custom_message: Mensagem personalizada para o usuário
        """
        # Log do erro
        error_msg = f"{context}: {str(error)}"
        
        if log_level.upper() == "ERROR":
            self.logger.error(error_msg, exc_info=True)
        elif log_level.upper() == "WARNING":
            self.logger.warning(error_msg, exc_info=True)
        else:
            self.logger.info(error_msg, exc_info=True)
        
        # Criar log detalhado com timestamp
        self._create_detailed_log(error, context)
        
        # Mostrar mensagem para o usuário se solicitado
        if show_message:
            self._show_user_message(error, context, custom_message)
    
    def _create_detailed_log(self, error: Exception, context: str):
        """Cria log detalhado com timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        log_filename = f'error-{timestamp}.txt'
        log_path = os.path.join(self.log_path, log_filename)
        
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"CONTEXTO: {context}\n")
            f.write(f"DATA/HORA: {timestamp}\n")
            f.write(f"ERRO: {str(error)}\n")
            f.write("TRACEBACK:\n")
            f.write(traceback.format_exc())
    
    def _show_user_message(self, error: Exception, context: str, custom_message: Optional[str] = None):
        """Mostra mensagem de erro para o usuário"""
        if custom_message:
            message = custom_message
        else:
            message = f"Não foi possível realizar: {context}\n\n"
            message += f"Erro: {str(error)}\n\n"
            message += f"Verifique o log mais recente na pasta '{self.log_path}' para mais informações."
        
        messagebox.showerror("Erro", message)
    
    def safe_execute(self, 
                    func: Callable, 
                    *args, 
                    context: str = "Operação",
                    show_message: bool = True,
                    log_level: str = "ERROR",
                    fallback: Optional[Callable] = None,
                    **kwargs) -> Any:
        """
        Executa uma função de forma segura com tratamento de erro
        
        Args:
            func: Função a ser executada
            *args: Argumentos posicionais
            context: Contexto da operação
            show_message: Se deve mostrar mensagem de erro
            log_level: Nível do log (ERROR, WARNING, INFO)
            fallback: Função alternativa em caso de erro
            **kwargs: Argumentos nomeados para a função
            
        Returns:
            Resultado da função ou None se houver erro
        """
        try:
            return func(*args, **kwargs)
        except Exception as error:
            self.handle_error(error, context, show_message, log_level)
            
            # Executar fallback se fornecido
            if fallback:
                try:
                    return fallback(*args, **kwargs)
                except Exception as fallback_error:
                    self.handle_error(fallback_error, f"{context} (fallback)", show_message, log_level)
            
            return None
    
    def handle_tkinter_error(self, error: Exception, context: str = "Interface"):
        """Tratamento específico para erros de interface Tkinter"""
        self.handle_error(
            error, 
            context, 
            show_message=True,
            custom_message=f"Não foi possível abrir a interface: {context}\n\n"
                         f"Verifique o log mais recente na pasta '{self.log_path}' para mais informações."
        )
    
    def handle_network_error(self, error: Exception, context: str = "Rede"):
        """Tratamento específico para erros de rede"""
        self.handle_error(
            error,
            context,
            show_message=True,
            custom_message=f"Erro de conexão: {context}\n\n"
                         f"Verifique sua conexão com a internet e tente novamente.\n"
                         f"Log detalhado disponível em: '{self.log_path}'"
        )
    
    def handle_file_error(self, error: Exception, context: str = "Arquivo"):
        """Tratamento específico para erros de arquivo"""
        self.handle_error(
            error,
            context,
            show_message=True,
            custom_message=f"Erro de arquivo: {context}\n\n"
                         f"Verifique se o arquivo existe e tem permissões adequadas.\n"
                         f"Log detalhado disponível em: '{self.log_path}'"
        )

# Instância global do error handler
error_handler = ErrorHandler() 
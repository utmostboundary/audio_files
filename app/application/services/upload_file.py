from dataclasses import dataclass

from app.application.auth.identity_provider import IdentityProvider
from app.application.file_manager import FileMetadata, FileManager
from app.application.gateways.audio_file import AudioFileGateway
from app.application.gateways.user import UserGateway
from app.application.transaction_manager import TransactionManager


@dataclass(frozen=True)
class UploadFileRequest:
    audio_name: str
    file: FileMetadata


class UploadFile:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        file_manager: FileManager,
        user_gateway: UserGateway,
        audio_file_gateway: AudioFileGateway,
        transaction_manager: TransactionManager,
    ):
        self._identity_provider = identity_provider
        self._file_manager = file_manager
        self._user_gateway = user_gateway
        self._audio_file_gateway = audio_file_gateway
        self._transaction_manager = transaction_manager

    async def execute(self, request: UploadFileRequest) -> None:
        user = await self._identity_provider.get_user()
        path = await self._file_manager.save(
            name=request.audio_name,
            metadata=request.file,
        )
        audio_file = user.upload_file(name=request.audio_name, path=path)
        self._audio_file_gateway.add(audio_file=audio_file)
        if not await self._transaction_manager.commit():
            await self._file_manager.delete(file_path=path)
